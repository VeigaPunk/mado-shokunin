#!/usr/bin/env python3
"""Normalised AST pin control; no subject execution or behavioral checks."""
import argparse
import ast
from pathlib import Path
import sys

class _DropDocstrings(ast.NodeTransformer):
    def _body(self, node):
        if (node.body and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)):
            del node.body[0]
        return self.generic_visit(node)

    visit_Module = _body
    visit_FunctionDef = _body
    visit_AsyncFunctionDef = _body
    visit_ClassDef = _body


class _DropUnusedAssignments(ast.NodeTransformer):
    def __init__(self):
        self.scopes = []

    def _scope(self, node, enabled=True, local=False):
        loaded = {item.id for item in ast.walk(node)
                  if isinstance(item, ast.Name) and isinstance(item.ctx, ast.Load)}
        protected = set()
        if local:
            for item in ast.walk(node):
                if isinstance(item, (ast.Global, ast.Nonlocal)):
                    protected.update(item.names)
        self.scopes.append((enabled, loaded, protected))
        result = self.generic_visit(node)
        self.scopes.pop()
        return result

    def visit_Module(self, node):
        return self._scope(node)

    def visit_FunctionDef(self, node):
        return self._scope(node, local=True)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        return self._scope(node, enabled=False)

    def _unused(self, target):
        enabled, loaded, protected = self.scopes[-1]
        if not enabled:
            return False
        if isinstance(target, ast.Name):
            return target.id not in loaded and target.id not in protected
        if isinstance(target, ast.Starred):
            return self._unused(target.value)
        if isinstance(target, (ast.Tuple, ast.List)):
            return bool(target.elts) and all(self._unused(item) for item in target.elts)
        return False

    def visit_Assign(self, node):
        node = self.generic_visit(node)
        node.targets = [target for target in node.targets if not self._unused(target)]
        return node if node.targets else None

    def visit_AnnAssign(self, node):
        node = self.generic_visit(node)
        return None if self._unused(node.target) else node

    visit_AugAssign = visit_AnnAssign

    def visit_NamedExpr(self, node):
        node = self.generic_visit(node)
        return node.value if self._unused(node.target) else node


def normalized_dump(source):
    tree = _DropDocstrings().visit(ast.parse(source))
    previous = ast.dump(tree)
    while True:
        tree = _DropUnusedAssignments().visit(tree)
        current = ast.dump(tree)
        if current == previous:
            return current
        previous = current


PIN = "Module(body=[Import(names=[alias(name='argparse')]), Import(names=[alias(name='re')]), Import(names=[alias(name='sys')]), Assign(targets=[Name(id='PRED_MARK', ctx=Store())], value=Call(func=Attribute(value=Name(id='re', ctx=Load()), attr='compile', ctx=Load()), args=[Constant(value='\\\\*\\\\*(PRED-[A-Za-z0-9._-]+)\\\\*\\\\*')])), Assign(targets=[Name(id='TOTAL', ctx=Store())], value=Call(func=Attribute(value=Name(id='re', ctx=Load()), attr='compile', ctx=Load()), args=[Constant(value='cases_pass=(\\\\d+)/(\\\\d+)')])), Assign(targets=[Name(id='SUMMARY', ctx=Store())], value=Call(func=Attribute(value=Name(id='re', ctx=Load()), attr='compile', ctx=Load()), args=[Constant(value='^[ \\\\t]*(PRED-[A-Za-z0-9._-]+)\\\\b[^\\\\n]*?cases_pass=(\\\\d+)/(\\\\d+)')])), Assign(targets=[Name(id='CASE_LINE', ctx=Store())], value=Call(func=Attribute(value=Name(id='re', ctx=Load()), attr='compile', ctx=Load()), args=[Constant(value='^CASE[ \\\\t]')])), FunctionDef(name='read_text', args=arguments(args=[arg(arg='path')]), body=[With(items=[withitem(context_expr=Call(func=Name(id='open', ctx=Load()), args=[Name(id='path', ctx=Load()), Constant(value='r')], keywords=[keyword(arg='encoding', value=Constant(value='utf-8'))]), optional_vars=Name(id='f', ctx=Store()))], body=[Return(value=Call(func=Attribute(value=Name(id='f', ctx=Load()), attr='read', ctx=Load())))])]), FunctionDef(name='parse_registration', args=arguments(args=[arg(arg='text')]), body=[Assign(targets=[Name(id='populations', ctx=Store())], value=Dict()), Assign(targets=[Name(id='problems', ctx=Store())], value=List(ctx=Load())), For(target=Name(id='para', ctx=Store()), iter=Call(func=Attribute(value=Name(id='re', ctx=Load()), attr='split', ctx=Load()), args=[Constant(value='\\\\n[ \\\\t]*\\\\n'), Name(id='text', ctx=Load())]), body=[Assign(targets=[Name(id='labels', ctx=Store())], value=List(ctx=Load())), For(target=Name(id='m', ctx=Store()), iter=Call(func=Attribute(value=Name(id='PRED_MARK', ctx=Load()), attr='finditer', ctx=Load()), args=[Name(id='para', ctx=Load())]), body=[If(test=Compare(left=Call(func=Attribute(value=Name(id='m', ctx=Load()), attr='group', ctx=Load()), args=[Constant(value=1)]), ops=[NotIn()], comparators=[Name(id='labels', ctx=Load())]), body=[Expr(value=Call(func=Attribute(value=Name(id='labels', ctx=Load()), attr='append', ctx=Load()), args=[Call(func=Attribute(value=Name(id='m', ctx=Load()), attr='group', ctx=Load()), args=[Constant(value=1)])]))])]), If(test=UnaryOp(op=Not(), operand=Name(id='labels', ctx=Load())), body=[Continue()]), Assign(targets=[Name(id='totals', ctx=Store())], value=SetComp(elt=Call(func=Name(id='int', ctx=Load()), args=[Call(func=Attribute(value=Name(id='m', ctx=Load()), attr='group', ctx=Load()), args=[Constant(value=2)])]), generators=[comprehension(target=Name(id='m', ctx=Store()), iter=Call(func=Attribute(value=Name(id='TOTAL', ctx=Load()), attr='finditer', ctx=Load()), args=[Name(id='para', ctx=Load())]), is_async=0)])), If(test=Compare(left=Call(func=Name(id='len', ctx=Load()), args=[Name(id='labels', ctx=Load())]), ops=[NotEq()], comparators=[Constant(value=1)]), body=[Expr(value=Call(func=Attribute(value=Name(id='problems', ctx=Load()), attr='append', ctx=Load()), args=[BinOp(left=Constant(value='paragraph names %d predicates beside %d total(s): %s'), op=Mod(), right=Tuple(elts=[Call(func=Name(id='len', ctx=Load()), args=[Name(id='labels', ctx=Load())]), Call(func=Name(id='len', ctx=Load()), args=[Name(id='totals', ctx=Load())]), Call(func=Attribute(value=Constant(value=','), attr='join', ctx=Load()), args=[Name(id='labels', ctx=Load())])], ctx=Load()))])), Continue()]), If(test=Compare(left=Call(func=Name(id='len', ctx=Load()), args=[Name(id='totals', ctx=Load())]), ops=[NotEq()], comparators=[Constant(value=1)]), body=[Expr(value=Call(func=Attribute(value=Name(id='problems', ctx=Load()), attr='append', ctx=Load()), args=[BinOp(left=Constant(value='predicate %s states %d distinct totals (%s)'), op=Mod(), right=Tuple(elts=[Subscript(value=Name(id='labels', ctx=Load()), slice=Constant(value=0), ctx=Load()), Call(func=Name(id='len', ctx=Load()), args=[Name(id='totals', ctx=Load())]), BoolOp(op=Or(), values=[Call(func=Attribute(value=Constant(value=','), attr='join', ctx=Load()), args=[GeneratorExp(elt=Call(func=Name(id='str', ctx=Load()), args=[Name(id='t', ctx=Load())]), generators=[comprehension(target=Name(id='t', ctx=Store()), iter=Call(func=Name(id='sorted', ctx=Load()), args=[Name(id='totals', ctx=Load())]), is_async=0)])]), Constant(value='none')])], ctx=Load()))])), Continue()]), Assign(targets=[Name(id='total', ctx=Store())], value=Call(func=Attribute(value=Name(id='totals', ctx=Load()), attr='pop', ctx=Load()))), If(test=BoolOp(op=And(), values=[Compare(left=Subscript(value=Name(id='labels', ctx=Load()), slice=Constant(value=0), ctx=Load()), ops=[In()], comparators=[Name(id='populations', ctx=Load())]), Compare(left=Subscript(value=Name(id='populations', ctx=Load()), slice=Subscript(value=Name(id='labels', ctx=Load()), slice=Constant(value=0), ctx=Load()), ctx=Load()), ops=[NotEq()], comparators=[Name(id='total', ctx=Load())])]), body=[Expr(value=Call(func=Attribute(value=Name(id='problems', ctx=Load()), attr='append', ctx=Load()), args=[BinOp(left=Constant(value='predicate %s stated twice with different totals (%d, %d)'), op=Mod(), right=Tuple(elts=[Subscript(value=Name(id='labels', ctx=Load()), slice=Constant(value=0), ctx=Load()), Subscript(value=Name(id='populations', ctx=Load()), slice=Subscript(value=Name(id='labels', ctx=Load()), slice=Constant(value=0), ctx=Load()), ctx=Load()), Name(id='total', ctx=Load())], ctx=Load()))])), Continue()]), Assign(targets=[Subscript(value=Name(id='populations', ctx=Load()), slice=Subscript(value=Name(id='labels', ctx=Load()), slice=Constant(value=0), ctx=Load()), ctx=Store())], value=Name(id='total', ctx=Load()))]), Return(value=Tuple(elts=[Name(id='populations', ctx=Load()), Name(id='problems', ctx=Load())], ctx=Load()))]), FunctionDef(name='main', args=arguments(), body=[Assign(targets=[Name(id='ap', ctx=Store())], value=Call(func=Attribute(value=Name(id='argparse', ctx=Load()), attr='ArgumentParser', ctx=Load()), keywords=[keyword(arg='description', value=Constant(value='Check that each receipt predicate population equals its registration target.'))])), Expr(value=Call(func=Attribute(value=Name(id='ap', ctx=Load()), attr='add_argument', ctx=Load()), args=[Constant(value='--registration')], keywords=[keyword(arg='required', value=Constant(value=True)), keyword(arg='metavar', value=Constant(value='PATH')), keyword(arg='help', value=Constant(value='lane registration file holding the predicate sentence(s)'))])), Expr(value=Call(func=Attribute(value=Name(id='ap', ctx=Load()), attr='add_argument', ctx=Load()), args=[Constant(value='receipts')], keywords=[keyword(arg='nargs', value=Constant(value='+')), keyword(arg='metavar', value=Constant(value='RECEIPT')), keyword(arg='help', value=Constant(value='counter receipt file(s) to check'))])), Assign(targets=[Name(id='args', ctx=Store())], value=Call(func=Attribute(value=Name(id='ap', ctx=Load()), attr='parse_args', ctx=Load()))), Try(body=[Assign(targets=[Name(id='reg_text', ctx=Store())], value=Call(func=Name(id='read_text', ctx=Load()), args=[Attribute(value=Name(id='args', ctx=Load()), attr='registration', ctx=Load())]))], handlers=[ExceptHandler(type=Tuple(elts=[Name(id='OSError', ctx=Load()), Name(id='UnicodeError', ctx=Load())], ctx=Load()), name='exc', body=[Expr(value=Call(func=Name(id='print', ctx=Load()), args=[BinOp(left=Constant(value='POPULATION verdict=UNREADABLE registration=%s error=%s'), op=Mod(), right=Tuple(elts=[Attribute(value=Name(id='args', ctx=Load()), attr='registration', ctx=Load()), Attribute(value=Attribute(value=Name(id='exc', ctx=Load()), attr='__class__', ctx=Load()), attr='__name__', ctx=Load())], ctx=Load()))])), Expr(value=Call(func=Name(id='print', ctx=Load()), args=[Constant(value='exit=2')])), Return(value=Constant(value=2))])]), Assign(targets=[Tuple(elts=[Name(id='populations', ctx=Store()), Name(id='problems', ctx=Store())], ctx=Store())], value=Call(func=Name(id='parse_registration', ctx=Load()), args=[Name(id='reg_text', ctx=Load())])), If(test=Name(id='problems', ctx=Load()), body=[For(target=Name(id='problem', ctx=Store()), iter=Name(id='problems', ctx=Load()), body=[Expr(value=Call(func=Name(id='print', ctx=Load()), args=[BinOp(left=Constant(value='POPULATION verdict=UNREADABLE registration=%s reason=%s'), op=Mod(), right=Tuple(elts=[Attribute(value=Name(id='args', ctx=Load()), attr='registration', ctx=Load()), Name(id='problem', ctx=Load())], ctx=Load()))]))]), Expr(value=Call(func=Name(id='print', ctx=Load()), args=[Constant(value='exit=2')])), Return(value=Constant(value=2))]), If(test=UnaryOp(op=Not(), operand=Name(id='populations', ctx=Load())), body=[Expr(value=Call(func=Name(id='print', ctx=Load()), args=[BinOp(left=Constant(value='POPULATION verdict=UNREADABLE registration=%s reason=no **PRED-...** sentence with a cases_pass=N/T total'), op=Mod(), right=Attribute(value=Name(id='args', ctx=Load()), attr='registration', ctx=Load()))])), Expr(value=Call(func=Name(id='print', ctx=Load()), args=[Constant(value='exit=2')])), Return(value=Constant(value=2))]), Expr(value=Call(func=Name(id='print', ctx=Load()), args=[BinOp(left=Constant(value='POPULATION registration=%s predicates=%s'), op=Mod(), right=Tuple(elts=[Attribute(value=Name(id='args', ctx=Load()), attr='registration', ctx=Load()), Call(func=Attribute(value=Constant(value=','), attr='join', ctx=Load()), args=[Call(func=Name(id='sorted', ctx=Load()), args=[Name(id='populations', ctx=Load())])])], ctx=Load()))])), Assign(targets=[Name(id='unreadable', ctx=Store())], value=Constant(value=0)), Assign(targets=[Name(id='mismatch', ctx=Store())], value=Constant(value=0)), Assign(targets=[Name(id='agreed', ctx=Store())], value=Constant(value=0)), For(target=Name(id='path', ctx=Store()), iter=Attribute(value=Name(id='args', ctx=Load()), attr='receipts', ctx=Load()), body=[Try(body=[Assign(targets=[Name(id='text', ctx=Store())], value=Call(func=Name(id='read_text', ctx=Load()), args=[Name(id='path', ctx=Load())]))], handlers=[ExceptHandler(type=Tuple(elts=[Name(id='OSError', ctx=Load()), Name(id='UnicodeError', ctx=Load())], ctx=Load()), name='exc', body=[AugAssign(target=Name(id='unreadable', ctx=Store()), op=Add(), value=Constant(value=1)), Expr(value=Call(func=Name(id='print', ctx=Load()), args=[BinOp(left=Constant(value='POPULATION receipt=%s verdict=UNREADABLE error=%s'), op=Mod(), right=Tuple(elts=[Name(id='path', ctx=Load()), Attribute(value=Attribute(value=Name(id='exc', ctx=Load()), attr='__class__', ctx=Load()), attr='__name__', ctx=Load())], ctx=Load()))])), Continue()])]), Assign(targets=[Name(id='lines', ctx=Store())], value=Call(func=Attribute(value=Name(id='text', ctx=Load()), attr='splitlines', ctx=Load()))), Assign(targets=[Name(id='summaries', ctx=Store())], value=List(ctx=Load())), For(target=Name(id='line', ctx=Store()), iter=Name(id='lines', ctx=Load()), body=[Assign(targets=[Name(id='m', ctx=Store())], value=Call(func=Attribute(value=Name(id='SUMMARY', ctx=Load()), attr='match', ctx=Load()), args=[Name(id='line', ctx=Load())])), If(test=Name(id='m', ctx=Load()), body=[Expr(value=Call(func=Attribute(value=Name(id='summaries', ctx=Load()), attr='append', ctx=Load()), args=[Tuple(elts=[Call(func=Attribute(value=Name(id='m', ctx=Load()), attr='group', ctx=Load()), args=[Constant(value=1)]), Call(func=Name(id='int', ctx=Load()), args=[Call(func=Attribute(value=Name(id='m', ctx=Load()), attr='group', ctx=Load()), args=[Constant(value=2)])]), Call(func=Name(id='int', ctx=Load()), args=[Call(func=Attribute(value=Name(id='m', ctx=Load()), attr='group', ctx=Load()), args=[Constant(value=3)])])], ctx=Load())]))])]), If(test=UnaryOp(op=Not(), operand=Name(id='summaries', ctx=Load())), body=[AugAssign(target=Name(id='unreadable', ctx=Store()), op=Add(), value=Constant(value=1)), Expr(value=Call(func=Name(id='print', ctx=Load()), args=[BinOp(left=Constant(value='POPULATION receipt=%s verdict=UNREADABLE reason=no PRED-... cases_pass=N/T summary line'), op=Mod(), right=Name(id='path', ctx=Load()))])), Continue()]), Assign(targets=[Name(id='case_lines', ctx=Store())], value=Call(func=Name(id='sum', ctx=Load()), args=[GeneratorExp(elt=Constant(value=1), generators=[comprehension(target=Name(id='line', ctx=Store()), iter=Name(id='lines', ctx=Load()), ifs=[Call(func=Attribute(value=Name(id='CASE_LINE', ctx=Load()), attr='match', ctx=Load()), args=[Name(id='line', ctx=Load())])], is_async=0)])])), For(target=Tuple(elts=[Name(id='pred', ctx=Store()), Name(id='num', ctx=Store()), Name(id='den', ctx=Store())], ctx=Store()), iter=Name(id='summaries', ctx=Load()), body=[If(test=Compare(left=Name(id='pred', ctx=Load()), ops=[NotIn()], comparators=[Name(id='populations', ctx=Load())]), body=[AugAssign(target=Name(id='mismatch', ctx=Store()), op=Add(), value=Constant(value=1)), Expr(value=Call(func=Name(id='print', ctx=Load()), args=[BinOp(left=Constant(value='POPULATION receipt=%s pred=%s cases_pass=%d/%d case_lines=%d registered=- agree=MISMATCH legs=registration_total'), op=Mod(), right=Tuple(elts=[Name(id='path', ctx=Load()), Name(id='pred', ctx=Load()), Name(id='num', ctx=Load()), Name(id='den', ctx=Load()), Name(id='case_lines', ctx=Load())], ctx=Load()))])), Continue()]), Assign(targets=[Name(id='registered', ctx=Store())], value=Subscript(value=Name(id='populations', ctx=Load()), slice=Name(id='pred', ctx=Load()), ctx=Load())), Assign(targets=[Name(id='legs', ctx=Store())], value=List(ctx=Load())), If(test=Compare(left=Name(id='case_lines', ctx=Load()), ops=[NotEq()], comparators=[Name(id='registered', ctx=Load())]), body=[Expr(value=Call(func=Attribute(value=Name(id='legs', ctx=Load()), attr='append', ctx=Load()), args=[Constant(value='case_lines')]))]), If(test=Compare(left=Name(id='den', ctx=Load()), ops=[NotEq()], comparators=[Name(id='registered', ctx=Load())]), body=[Expr(value=Call(func=Attribute(value=Name(id='legs', ctx=Load()), attr='append', ctx=Load()), args=[Constant(value='denominator')]))]), If(test=Name(id='legs', ctx=Load()), body=[AugAssign(target=Name(id='mismatch', ctx=Store()), op=Add(), value=Constant(value=1)), Expr(value=Call(func=Name(id='print', ctx=Load()), args=[BinOp(left=Constant(value='POPULATION receipt=%s pred=%s cases_pass=%d/%d case_lines=%d registered=%d agree=MISMATCH legs=%s'), op=Mod(), right=Tuple(elts=[Name(id='path', ctx=Load()), Name(id='pred', ctx=Load()), Name(id='num', ctx=Load()), Name(id='den', ctx=Load()), Name(id='case_lines', ctx=Load()), Name(id='registered', ctx=Load()), Call(func=Attribute(value=Constant(value=','), attr='join', ctx=Load()), args=[Name(id='legs', ctx=Load())])], ctx=Load()))]))], orelse=[AugAssign(target=Name(id='agreed', ctx=Store()), op=Add(), value=Constant(value=1)), Expr(value=Call(func=Name(id='print', ctx=Load()), args=[BinOp(left=Constant(value='POPULATION receipt=%s pred=%s cases_pass=%d/%d case_lines=%d registered=%d agree=ok'), op=Mod(), right=Tuple(elts=[Name(id='path', ctx=Load()), Name(id='pred', ctx=Load()), Name(id='num', ctx=Load()), Name(id='den', ctx=Load()), Name(id='case_lines', ctx=Load()), Name(id='registered', ctx=Load())], ctx=Load()))]))])])]), If(test=Name(id='unreadable', ctx=Load()), body=[Assign(targets=[Tuple(elts=[Name(id='verdict', ctx=Store()), Name(id='rc', ctx=Store())], ctx=Store())], value=Tuple(elts=[Constant(value='UNREADABLE'), Constant(value=2)], ctx=Load()))], orelse=[If(test=Name(id='mismatch', ctx=Load()), body=[Assign(targets=[Tuple(elts=[Name(id='verdict', ctx=Store()), Name(id='rc', ctx=Store())], ctx=Store())], value=Tuple(elts=[Constant(value='FAIL'), Constant(value=1)], ctx=Load()))], orelse=[Assign(targets=[Tuple(elts=[Name(id='verdict', ctx=Store()), Name(id='rc', ctx=Store())], ctx=Store())], value=Tuple(elts=[Constant(value='PASS'), Constant(value=0)], ctx=Load()))])]), Expr(value=Call(func=Name(id='print', ctx=Load()), args=[BinOp(left=Constant(value='POPULATION verdict=%s receipts=%d agree=%d mismatch=%d unreadable=%d'), op=Mod(), right=Tuple(elts=[Name(id='verdict', ctx=Load()), Call(func=Name(id='len', ctx=Load()), args=[Attribute(value=Name(id='args', ctx=Load()), attr='receipts', ctx=Load())]), Name(id='agreed', ctx=Load()), Name(id='mismatch', ctx=Load()), Name(id='unreadable', ctx=Load())], ctx=Load()))])), Expr(value=Call(func=Name(id='print', ctx=Load()), args=[BinOp(left=Constant(value='exit=%d'), op=Mod(), right=Name(id='rc', ctx=Load()))])), Return(value=Name(id='rc', ctx=Load()))]), If(test=Compare(left=Name(id='__name__', ctx=Load()), ops=[Eq()], comparators=[Constant(value='__main__')]), body=[Expr(value=Call(func=Attribute(value=Name(id='sys', ctx=Load()), attr='exit', ctx=Load()), args=[Call(func=Name(id='main', ctx=Load()))]))])])"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checker', required=True)
    args = parser.parse_args()
    try:
        actual = normalized_dump(Path(args.checker).read_bytes())
    except (OSError, SyntaxError, ValueError, UnicodeError) as error:
        print('NORM_PIN checker unreadable: %s' % error)
        return 1
    if actual != PIN:
        print('NORM_PIN checker MISMATCH')
        return 1
    print('NORM_PIN normalized pristine checker AST dump matches')
    return 0


if __name__ == '__main__':
    sys.exit(main())
