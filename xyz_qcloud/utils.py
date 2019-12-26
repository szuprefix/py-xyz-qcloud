# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

class Accessor(str):
    '''
    A string describing a path from one object to another via attribute/index
    accesses. For convenience, the class has an alias `.A` to allow for more concise code.

    Relations are separated by a ``.`` character.
    '''
    SEPARATOR = '.'

    def resolve(self, context, safe=True, quiet=False):
        '''
        Return an object described by the accessor by traversing the attributes
        of *context*.

        Lookups are attempted in the following order:

         - dictionary (e.g. ``obj[related]``)
         - attribute (e.g. ``obj.related``)
         - list-index lookup (e.g. ``obj[int(related)]``)

        Callable objects are called, and their result is used, before
        proceeding with the resolving.

        Example::

            >>> x = Accessor('__len__')
            >>> x.resolve('brad')
            4
            >>> x = Accessor('0.upper')
            >>> x.resolve('brad')
            'B'

        Arguments:
            context (object): The root/first object to traverse.
            safe (bool): Don't call anything with `alters_data = True`
            quiet (bool): Smother all exceptions and instead return `None`

        Returns:
            target object

        Raises:
            TypeError`, `AttributeError`, `KeyError`, `ValueError`
            (unless `quiet` == `True`)
        '''
        try:
            current = context
            for bit in self.bits:
                try:  # dictionary lookup
                    current = current[bit]
                except (TypeError, AttributeError, KeyError):
                    try:  # attribute lookup
                        current = getattr(current, bit)
                    except (TypeError, AttributeError):
                        try:  # list-index lookup
                            current = current[int(bit)]
                        except (IndexError,  # list index out of range
                                ValueError,  # invalid literal for int()
                                KeyError,    # dict without `int(bit)` key
                                TypeError,   # unsubscriptable object
                                ):
                            raise ValueError('Failed lookup for key [%s] in %r'
                                             ', when resolving the accessor %s' % (bit, current, self)
                                             )
                if callable(current):
                    if safe and getattr(current, 'alters_data', False):
                        raise ValueError('refusing to call %s() because `.alters_data = True`'
                                         % repr(current))
                    if not getattr(current, 'do_not_call_in_templates', False):
                        current = current()
                # important that we break in None case, or a relationship
                # spanning across a null-key will raise an exception in the
                # next iteration, instead of defaulting.
                if current is None:
                    break
            return current
        except:
            if not quiet:
                raise

    @property
    def bits(self):
        if self == '':
            return ()
        return self.split(self.SEPARATOR)

    def get_field(self, model):
        '''Return the django model field for model in context, following relations'''
        if not hasattr(model, '_meta'):
            return

        field = None
        from django.core.exceptions import FieldDoesNotExist
        for bit in self.bits:
            try:
                field = model._meta.get_field(bit)
            except FieldDoesNotExist:
                break
            if hasattr(field, 'rel') and hasattr(field.rel, 'to'):
                model = field.rel.to
                continue

        return field

    def penultimate(self, context, quiet=True):
        '''
        Split the accessor on the right-most dot '.', return a tuple with:
         - the resolved left part.
         - the remainder

        Example::

            >>> Accessor('a.b.c').penultimate({'a': {'a': 1, 'b': {'c': 2, 'd': 4}}})
            ({'c': 2, 'd': 4}, 'c')

        '''
        path, _, remainder = self.rpartition('.')
        return A(path).resolve(context, quiet=quiet), remainder


A = Accessor  # alias
