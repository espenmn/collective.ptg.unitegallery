# -*- coding: utf-8 -*-
"""Init and utils."""
import logging
from zope.i18nmessageid import MessageFactory
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.plonetruegallery.browser.views.display import BaseDisplayType
from collective.plonetruegallery.browser.views.display import jsbool
from collective.plonetruegallery.interfaces import IBaseSettings
from zope.schema.interfaces import IField, IBool, IChoice, ITextLine, IInt, IFloat
from zope import schema
from plone.memoize.view import memoize
LOG = logging.getLogger(__name__)
_ = MessageFactory('collective.ptg.unitegallery')


class UniteGalleryCommon(BaseDisplayType):
    name = u"unitegallery"
    theme = 'default'
    schema = None
    description = _(u"label_unitegallery_display_type",
        default=u"Unite Gallery")
    typeStaticFilesRelative = '++resource++ptg.unitegallery'

    def theme_js_url(self):
        return '++resource++ptg.unitegallery/themes/'+self.theme+'/ug-theme-'+self.theme+'.js'
        
    def theme_css(self):
        if self.theme != 'default':
            return ''
        return """
<link rel="stylesheet" type="text/css"
    href="%(base_url)s/++resource++ptg.unitegallery/themes/%(theme)s/ug-theme-%(theme)s.css" media="screen" />
""" % {
    'base_url': self.typeStaticFiles,
    'theme':self.theme,
    }
        
    def skin_css(self):
        skin = self.settings.gallery_skin
        if skin == 'default':
            return ''
        return """
<link rel="stylesheet" type="text/css"
    href="%(base_url)s/++resource++ptg.unitegallery/skins/%(skin)s/%(skin)s.css" media="screen" />
""" % {
    'base_url': self.typeStaticFiles,
    'skin':skin,
    }

    def javascript(self):
        return u"""
<script type="text/javascript">
requirejs(["%(base_url)s/js/unitegallery.min.js"], function(util) {
    requirejs(["%(theme_js_url)s"], function(util) {
        (function($){
            $(document).ready(function() {
                $("#gallery").each(function(){
                        $(this).unitegallery({
			            %(gallery_theme)s
			            %(theme_options)s
			        });
			    });
            });
        })(jQuery);
    });
});
</script>
    """ % {
            'start_index_index': self.start_image_index,
            'staticFiles':  self.staticFiles,
            'base_url': self.typeStaticFiles,
            'gallery_theme':self.theme != 'default' and 'gallery_theme: "'+self.theme+'",' or '',
            'theme_js_url':self.theme_js_url(),
            'theme_options':',\n'.join(k+':'+v for k,v in self.theme_options().items()),
        }

    def theme_options(self):
        data = {}
        for name in self.schema.names():
            field = self.schema[name]
            if not IField.providedBy(field):
                continue
            value = getattr(self.settings, name, None)
            if value == None:
                continue
            name = name.replace(self.theme+'_','',1)
            if IBool.providedBy(field):
                data[name] = jsbool(value)
            elif IChoice.providedBy(field) or ITextLine.providedBy(field):
                data[name] = '"'+value+'"'
            elif IInt.providedBy(field) or IFloat.providedBy(field):
                data[name] = str(value)
        return data


    def css(self):
        return u"""
<link rel="stylesheet" type="text/css"
    href="%(base_url)s/css/unite-gallery.css" media="screen" />
%(theme_css)s
""" % {
        'staticFiles': self.staticFiles,
        'base_url': self.typeStaticFiles,
        'theme_css' : self.theme_css(),
        'skin_css' : self.skin_css(),
        }


