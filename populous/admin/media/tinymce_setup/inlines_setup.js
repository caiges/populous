var INLINE_COUNT = 0;   // Global inline count
var INLINE_HASH = {};

/*
    Inline Class Stuff
*/
function Inline(inline, app_label, model_name, model_pk, field_name) {
    INLINE_COUNT += 1;
    this.id = INLINE_COUNT;
    
    this.inline = inline;
    this.model_app_label = app_label;
    this.model_name = model_name;
    this.field_name = field_name;
    this.model_pk = model_pk;
    this.attrs = this._get_attrs();

    bits = this.getAttr('type').split(".");
    this.app_label = bits[0];
    this.inline_name = bits[1];
    
    this.el = $('<div class="inline" id="inline-' + this.id + '"></div>').css('cursor', 'pointer');
    $(this.inline).after(this.el);
    this.el.append($(this.inline));
    //$(this.inline).replaceWith(this.el);
    this.el.parent('p').replaceWith(this.el);
};

Inline.prototype._get_attrs = function() {
    /*  Create a simple Object holding our attributes */
    attrs = {};
    for (var i=0; i < this.inline.attributes.length; i++) {
        attr = this.inline.attributes[i];
        attrs[attr.name] = attr.value;
    }
    return attrs;
};

Inline.prototype.repr = function() {
    /* Blah */
    return {
        id:                 this.id,
        model_app_label:    this.model_app_label,
        model_name:         this.model_name,
        model_pk:           this.model_pk,
        field_name:         this.field_name,
        attrs:              $.toJSON(this.attrs)
    }
};

Inline.prototype.getAttr = function(attr, rtn) {
    /* Attempts to get the attribute, returns ``rtn`` if not found. */
    if (typeof(rtn) == "undefined")
        rtn = null;
    
    val = this.attrs[attr];
    if (val == null)
        return rtn;
    else
        return val;
};

Inline.prototype.render = function() {
    /* Just a simple wrapper to render the inline via ajax. */
    var self = this;
    $.post('/admin/inlines/render/', this.repr(), function(data) {
        $(self.inline).after($(data));
        self.el.children().mousedown(select_func);
    });
};

function CustomFileBrowser(field_name, url, type, win) {

    var cmsURL = "/admin/filebrowser/?pop=2";
    cmsURL = cmsURL + "&type=" + type;
    
    tinyMCE.activeEditor.windowManager.open({
        file: cmsURL,
        width: 820,  // Your dimensions may differ - toy around with them!
        height: 500,
        resizable: "yes",
        scrollbars: "yes",
        inline: "no",  // This parameter only has an effect if you use the inlinepopups plugin!
        close_previous: "no",
    }, {
        window: win,
        input: field_name,
        editor_id: tinyMCE.selectedInstance.editorId,
    });
    return false;
}

var select_func = function() {
    console.log("Mousedown");
    el = $(this).parent('.inline');
    tinyMCE.activeEditor.selection.select(el[0]);
    return el[0];
};

function MCEInit() {
    bits = document.location.pathname.split('/');
    app_label = bits[bits.length - 4];
    model_name = bits[bits.length - 3];
    model_pk = bits[bits.length - 2];
    
    $('iframe').each(function() {
        // Wow, this in convoluted...
        field_name = $(this).parents('div.form-row').children('label').attr('for').split('id_')[1];
        $(this).contents().find('inline').each(function() {
            inline = new Inline(this, app_label, model_name, model_pk, field_name);
            INLINE_HASH[inline.id] = inline;
            inline.render();
        });
    });

    $('iframe').contents().find('#tinymce').bind('DOMNodeInserted', function(e) {
        // This guy gets called when we drag the inline around.
        if ($(e.target).hasClass('inline')) {
            console.log('You moved an inline.  Rebinding event listeners!');
            $(e.target).children().mousedown(select_func);
        }
    });
};

tinyMCE.init({
    mode: "textareas",
    oninit : "MCEInit",
    //elements: "summary, body",
    theme: "advanced",
    language: "en",
    skin: "o2k7",
    //browsers: "gecko",
    dialog_type: "window",
    object_resizing: true,
    //cleanup_on_startup: true,
    //forced_root_block: "p",
    remove_trailing_nbsp: true,
    content_css: "/admin_media/tinymce_setup/css_grappelli/content.css",
    editor_css: "/admin_media/tinymce_setup/css_grappelli/editor.css",
    popup_css: "/admin_media/tinymce_setup/css_grappelli/popup.css",
    visualchars_css: "/admin_media/tinymce_setup/css_grappelli/content_visualchars.css",
    theme_advanced_toolbar_location: "top",
    theme_advanced_toolbar_align: "left",
    theme_advanced_statusbar_location: "none",
    theme_advanced_buttons1: "formatselect,styleselect,bold,italic,underline,bullist,numlist,undo,redo,link,unlink,image,code,template,pasteword,media,youtube,charmap,visualchars,fullscreen",
    theme_advanced_buttons2: "",
    theme_advanced_buttons3: "",
    theme_advanced_path: false,
    theme_advanced_blockformats: "p,h2,h3,h4,div,code,pre,blockquote,inline",
    theme_advanced_styles: "[all] clearfix=clearfix;[p] small=small;[img] Image left-aligned=img_left;[img] Image left-aligned (nospace)=img_left_nospacetop;[img] Image right-aligned=img_right;[img] Image right-aligned (nospace)=img_right_nospacetop;[img] Image Block=img_block;[img] Image Block (nospace)=img_block_nospacetop;[div] column span-2=column span-2;[div] column span-4=column span-4;[div] column span-8=column span-8",
    width: '700',
    height: '200',
    plugins: "advimage,advlink,fullscreen,visualchars,paste,media,template,searchreplace,youtube,noneditable",
    noneditable_noneditable_class: "inline",
    theme_advanced_styles: "Image left-aligned=img_left;Image left-aligned (nospace)=img_left_nospacetop;Image right-aligned=img_right;Image right-aligned (nospace)=img_right_nospacetop;Image Block=img_block",
    advimage_update_dimensions_onchange: true,
    advlink_styles: "intern=internal;extern=external",
    file_browser_callback: "CustomFileBrowser",
    //cleanup_callback : "CustomCleanup",
    indentation : '10px',
    fix_list_elements : true,
    relative_urls: false,
    remove_script_host : true,
    accessibility_warnings : false,
    template_templates : [
        {
            title : "2 Columns (300px / 300px)",
            src : "/tinymce-templates/snippets/2col/",
            description : "Symmetrical 2 Columns."
        },
        {
            title : "2 Columns (420px / 140px)",
            src : "/tinymce-templates/snippets/2col_left/",
            description : "Asymmetrical 2 Columns: big left, small right."
        },
        {
            title : "2 Columns (140px / 420px)",
            src : "/tinymce-templates/snippets/2col_right/",
            description : "Asymmetrical 2 Columns: small left, big right."
        },
        {
            title : "3 Columns (300px / 300px)",
            src : "/tinymce-templates/snippets/3col/",
            description : "3 Columns."
        },
    ],
    valid_elements : "" +
    "-p," + 
    "-inline,"+
    "a[href|target=_blank|class]," +
    "-strong/-b," +
    "-em/-i," +
    "-u," + 
    "-ol," + 
    "-ul," + 
    "-li," + 
    "br," + 
    "-inline[type|template]," +
    "img[class|src|alt=|width|height]," + 
    "-h2,-h3,-h4," + 
    "-pre," +
    "-code," + 
    "-div",
    extended_valid_elements: "" + 
    "a[name|class|href|target|title|onclick]," + 
    "img[class|src|border=0|alt|title|hspace|vspace|width|height|align|onmouseover|onmouseout|name]," + 
    "br[clearfix]," + 
    "-p[class<clearfix?summary?code]," + 
    "h2[class<clearfix],h3[class<clearfix],h4[class<clearfix]," + 
    "ul[class<clearfix],ol[class<clearfix]," + 
    "div[class],",
    valid_child_elements : "" + 
    "h1/h2/h3/h4/h5/h6/a[%itrans_na]," + 
    "table[thead|tbody|tfoot|tr|td]," + 
    "strong/b/p/div/em/i/td[%itrans|#text]," + 
    "body[%btrans|#text]",
});


