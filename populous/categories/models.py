from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    parent = models.ForeignKey('self', related_name='parent_rel', null=True, verbose_name=_('parent'))
    name = models.CharField(_('name'), max_length=200)
    representation = models.CharField(_('representation'), max_length=500, editable=False, db_index=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        unique_together = (('parent', 'name'),)
        ordering = ('representation',)
    
    def __unicode__(self):
        return self.representation
    
    def save(self):
        # TODO Model validation when availible
        super(Category, self).save()
        self._refresh_representation()
    
    def get_children(self):
        """
        Returns a list of Category objects that are direct children of the current Category object.
        """
        if not hasattr(self, '_children'):
            self._children = Category.objects.filter(parent__exact=self)
        return self._children
    
    def get_all_children(self, **kwargs):
        """
        Returns a list of all Category objects that children of the current Category object.
        """ 
        return Category.objects.filter(representation__startswith= self.representation + "/")
    
    def get_parents(self):
        if not hasattr(self, '_parents'):
            self._parents = []
            current = self
            while current.parent:
                self._parents.append(current.parent)
                current = current.parent
        return self._parents
    
    def _refresh_representation(self):
        """
        Forms tree representation for current Category object based on its parent object and refreshes all children representations.
        """
        if not self.parent:
            representation = "/"
        else:
            representation = self.name + "/"
            if self.parent.id != 1:
                representation = self.parent.representation + representation
        if representation != self.representation:
            self.representation = representation
            self.save()
        for child in self.get_children():
            child._refresh_representation()