/* ExecOracleGkeep (round 43 w1): minimal Wayland shm client for the nested-compositor oracle.
 *
 * Creates ONE xdg_toplevel with a shm buffer and an application id, and never asks for a size:
 * no set_min_size / set_max_size / set_fullscreen / set_maximized / set_fullscreen, and the
 * buffer size is a hint only. Written from the wlroots/xdg-shell tutorials; the xdg-shell
 * protocol code is generated at build time by wayland-scanner from the system XML.
 *
 * usage: gkeep-shm --app-id org.omarchy.gkeep [--width 200] [--height 200]
 */
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <wayland-client.h>
#include "xdg-shell-client-protocol.h"

struct state {
    struct wl_display *display;
    struct wl_registry *registry;
    struct wl_compositor *compositor;
    struct wl_shm *shm;
    struct xdg_wm_base *wm_base;
    struct wl_surface *surface;
    struct xdg_surface *xdg_surface;
    struct xdg_toplevel *toplevel;
    struct wl_buffer *buffer;
    int configured;
    int width, height;
    int min_w, min_h;
    const char *app_id;
};

static int create_shm_file(size_t size) {
    int fd = memfd_create("gkeep-shm", MFD_CLOEXEC);
    if (fd < 0) { perror("memfd_create"); exit(1); }
    if (ftruncate(fd, (off_t)size) < 0) { perror("ftruncate"); exit(1); }
    return fd;
}

static void wm_base_ping(void *data, struct xdg_wm_base *b, uint32_t serial) {
    (void)data;
    xdg_wm_base_pong(b, serial);
}
static const struct xdg_wm_base_listener wm_base_listener = { .ping = wm_base_ping };

static void xdg_surface_configure(void *data, struct xdg_surface *xs, uint32_t serial) {
    struct state *s = data;
    xdg_surface_ack_configure(xs, serial);
    if (!s->configured) {
        s->configured = 1;
        wl_surface_attach(s->surface, s->buffer, 0, 0);
        wl_surface_damage_buffer(s->surface, 0, 0, s->width, s->height);
        wl_surface_commit(s->surface);
        fprintf(stderr, "CLIENT_READY app_id=%s buffer=%dx%d\n", s->app_id, s->width, s->height);
    }
}
static const struct xdg_surface_listener xdg_surface_listener = { .configure = xdg_surface_configure };

static void toplevel_configure(void *data, struct xdg_toplevel *t, int32_t w, int32_t h,
                               struct wl_array *states) {
    struct state *s = data;
    (void)t; (void)states;
    /* Record only: the client never constrains its size. */
    fprintf(stderr, "TOPLEVEL_CONFIGURE w=%d h=%d\n", w, h);
    if (w > 0 && h > 0) { /* keep drawing buffer as-is; buffer is a hint */ }
    (void)s;
}
static void toplevel_close(void *data, struct xdg_toplevel *t) {
    (void)t; (void)data;
    fprintf(stderr, "TOPLEVEL_CLOSE\n");
    exit(0);
}
static void toplevel_bounds(void *data, struct xdg_toplevel *t, int32_t w, int32_t h) {
    (void)data; (void)t; (void)w; (void)h;
}
static void toplevel_capabilities(void *data, struct xdg_toplevel *t, struct wl_array *caps) {
    (void)data; (void)t; (void)caps;
}
static void toplevel_configure_bounds(void *data, struct xdg_toplevel *t, int32_t w, int32_t h) {
    (void)data; (void)t; (void)w; (void)h;
}
static void toplevel_wm_capabilities(void *data, struct xdg_toplevel *t, struct wl_array *caps) {
    (void)data; (void)t; (void)caps;
}
static const struct xdg_toplevel_listener toplevel_listener = {
    .configure = toplevel_configure,
    .close = toplevel_close,
    .configure_bounds = toplevel_configure_bounds,
    .wm_capabilities = toplevel_wm_capabilities,
};

static void registry_global(void *data, struct wl_registry *reg, uint32_t name,
                            const char *iface, uint32_t version) {
    struct state *s = data;
    if (!strcmp(iface, wl_compositor_interface.name))
        s->compositor = wl_registry_bind(reg, name, &wl_compositor_interface, version < 4 ? version : 4);
    else if (!strcmp(iface, wl_shm_interface.name))
        s->shm = wl_registry_bind(reg, name, &wl_shm_interface, 1);
    else if (!strcmp(iface, xdg_wm_base_interface.name)) {
        s->wm_base = wl_registry_bind(reg, name, &xdg_wm_base_interface, version < 6 ? version : 6);
        xdg_wm_base_add_listener(s->wm_base, &wm_base_listener, s);
    }
}
static void registry_global_remove(void *data, struct wl_registry *reg, uint32_t name) {
    (void)data; (void)reg; (void)name;
}
static const struct wl_registry_listener registry_listener = {
    .global = registry_global, .global_remove = registry_global_remove,
};

int main(int argc, char **argv) {
    struct state s = { .width = 200, .height = 200, .app_id = "org.omarchy.gkeep" };
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--app-id") && i + 1 < argc) s.app_id = argv[++i];
        else if (!strcmp(argv[i], "--width") && i + 1 < argc) s.width = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--height") && i + 1 < argc) s.height = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--min-size") && i + 1 < argc) { sscanf(argv[++i], "%dx%d", &s.min_w, &s.min_h); }
        else { fprintf(stderr, "unknown arg %s\n", argv[i]); return 2; }
    }
    s.display = wl_display_connect(NULL);
    if (!s.display) { fprintf(stderr, "CONNECT_FAILED\n"); return 1; }
    s.registry = wl_display_get_registry(s.display);
    wl_registry_add_listener(s.registry, &registry_listener, &s);
    if (wl_display_roundtrip(s.display) < 0) { fprintf(stderr, "ROUNDTRIP_FAILED\n"); return 1; }
    if (!s.compositor || !s.shm || !s.wm_base) {
        fprintf(stderr, "MISSING_GLOBALS compositor=%p shm=%p xdg_wm_base=%p\n",
                (void *)s.compositor, (void *)s.shm, (void *)s.wm_base);
        return 1;
    }

    int stride = s.width * 4, size = stride * s.height;
    int fd = create_shm_file(size);
    uint32_t *pix = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (pix == MAP_FAILED) { perror("mmap"); return 1; }
    for (int i = 0; i < s.width * s.height; i++) pix[i] = 0xFF2E3440u; /* opaque ARGB, arbitrary */
    struct wl_shm_pool *pool = wl_shm_create_pool(s.shm, fd, size);
    s.buffer = wl_shm_pool_create_buffer(pool, 0, s.width, s.height, stride, WL_SHM_FORMAT_ARGB8888);
    wl_shm_pool_destroy(pool);
    close(fd);

    s.surface = wl_compositor_create_surface(s.compositor);
    s.xdg_surface = xdg_wm_base_get_xdg_surface(s.wm_base, s.surface);
    xdg_surface_add_listener(s.xdg_surface, &xdg_surface_listener, &s);
    s.toplevel = xdg_surface_get_toplevel(s.xdg_surface);
    xdg_toplevel_add_listener(s.toplevel, &toplevel_listener, &s);
    xdg_toplevel_set_app_id(s.toplevel, s.app_id);
    xdg_toplevel_set_title(s.toplevel, "gkeep-oracle-probe");
    /* deliberately no set_min_size / set_max_size / set_fullscreen / set_maximized unless asked */
    if (s.min_w > 0 && s.min_h > 0) {
        xdg_toplevel_set_min_size(s.toplevel, s.min_w, s.min_h);
        fprintf(stderr, "CLIENT_MIN_SIZE %dx%d\n", s.min_w, s.min_h);
    }
    wl_surface_attach(s.surface, s.buffer, 0, 0);
    wl_surface_damage_buffer(s.surface, 0, 0, s.width, s.height);
    wl_surface_commit(s.surface);

    while (wl_display_dispatch(s.display) != -1) { }
    fprintf(stderr, "DISPLAY_DISPATCH_END\n");
    return 0;
}
