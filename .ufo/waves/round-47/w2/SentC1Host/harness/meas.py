import resource, subprocess, sys, time
t=time.time(); p=subprocess.run(sys.argv[1:], capture_output=True); w=time.time()-t
u=resource.getrusage(resource.RUSAGE_CHILDREN)
sys.stderr.write("rc=%d wall=%.2fs rss_kb=%d out_tail=%r err_tail=%r\n" % (p.returncode, w, u.ru_maxrss, p.stdout[-120:], p.stderr[-160:]))
