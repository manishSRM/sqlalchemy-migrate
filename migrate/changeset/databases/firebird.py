"""
   Firebird database specific implementations of changeset classes.
"""
from sqlalchemy.databases import firebird as sa_base

from migrate.changeset import ansisql, exceptions


FBSchemaGenerator = sa_base.FBSchemaGenerator


class FBColumnGenerator(FBSchemaGenerator, ansisql.ANSIColumnGenerator):
    """Firebird column generator implementation."""


class FBColumnDropper(ansisql.ANSIColumnDropper):
    """Firebird column dropper implementation."""

    def visit_column(self, column):
        table = self.start_alter_table(column)
        self.append('DROP %s' % self.preparer.format_column(column))
        self.execute()


class FBSchemaChanger(ansisql.ANSISchemaChanger):
    """Firebird schema changer implementation."""

    def visit_table(self, table):
        """Rename table not supported"""
        raise exceptions.NotSupportedError(
            "Firebird does not support renaming tables.")

    def _visit_column_name(self, table, column, delta):
        self.start_alter_table(table)
        col_name = self.preparer.quote(delta.current_name, table.quote)
        new_name = self.preparer.format_column(delta.result_column)
        self.append('ALTER COLUMN %s TO %s' % (col_name, new_name))

    def _visit_column_nullable(self, table, column, delta):
        """Changing NULL is not supported"""
        # TODO: http://www.firebirdfaq.org/faq103/
        raise exceptions.NotSupportedError(
            "Firebird does not support altering NULL bevahior.")


class FBConstraintGenerator(ansisql.ANSIConstraintGenerator):
    """Firebird constraint generator implementation."""


class FBConstraintDropper(ansisql.ANSIConstraintDropper):
    """Firebird constaint dropper implementation."""

    def cascade_constraint(self, constraint):
        """Cascading constraints is not supported"""
        raise exceptions.NotSupportedError(
            "Firebird does not support cascading constraints")


class FBDialect(ansisql.ANSIDialect):
    columngenerator = FBColumnGenerator
    columndropper = FBColumnDropper
    schemachanger = FBSchemaChanger
    constraintgenerator = FBConstraintGenerator
    constraintdropper = FBConstraintDropper
