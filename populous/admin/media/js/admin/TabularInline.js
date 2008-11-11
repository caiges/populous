$(document).ready(function(){
    
    /// BEHAVIOUR
    /// DELETED ITEMS will be moved to the end of the group.
    /// In case of an Error, deleted stay at this position.
    /// EXTRA ITEMS stay at their position, if they are not empty.
    /// In case of an Error, empty extra items are moved to the end of
    /// the list (just before predeleted items).
    
    $('div[name="inlinegrouptabular"] a.addhandler').bind("click", function(){
        clone_item = $(this).parent().parent().parent().find('.items tr:last')
        new_item = $(clone_item).clone(true).insertAfter($(clone_item));
        /// remove 1 from length because of the table-header
        items = $(this).parent().parent().parent().find('.items tr').length - 1;
        /// replace IDs, NAMEs, HREFs & FORs ...
        new_html = new_item.html().replace(/-\d+-/g, "-" + parseInt(items - 1) + "-");
        new_item.html(new_html);
        /// reset all form-fields
        new_item.find(':input').val('');
        /// set TOTAL_FORMS to number of items
        new_item.parent().parent().parent().parent().find('input[id*="TOTAL_FORMS"]').val(parseInt(items));
        /// FILEBROWSER SPECIFIC: remove image preview
        new_item.find('img.preview').each(function(i) {
            $(this).attr('src', '');
            $(this).parent().parent().hide();
        });
        /// remove error-lists and error-classes
        new_item.find('ul.errorlist').remove();
        new_item.find('div[class*="errors"]').removeClass("errors");
        /// remove delete-button and button view on site
        new_item.find('a.deletelink').remove();
        new_item.find('a.viewsitelink').remove();
    });
    
    // REORDER TBODIES
    $('div[name="inlinegrouptabular"].sortable table').each(function(i) {
        items = new Array();
        predeleted_items_count = $(this).find('input[name*="DELETE"]:checked').length;
        empty_counter = $(this).find('input[value][id*="order"]').length - predeleted_items_count;
        $(this).find('tbody').each(function(i) {
            /// if order field is not set (which is for empty items), set the counter
            /// so that these fields are shown before the predeleted_items
            if ($(this).find('input[id*="order"]').val()) {
                order_value = $(this).find('input[id*="order"]').val();
            } else {
                order_value = empty_counter;
                empty_counter++;
            }
            $(this).find('input[id*="order"]').val(order_value);
            items[parseInt(order_value)] = $(this);
        });
        items.sort();
        $(this).children('tbody').remove();
        for (var i = 0; i < items.length; i++) {
            predelete_flag = $(items[i]).find('input[name*="DELETE"]:checked').length;
            if (predelete_flag) {
                $(items[i]).removeClass('item');
                $(items[i]).addClass('predelete-item');
            }
            $(this).append(items[i]);
        } 
    });
    
    /// DELETELINK
    $('div[name="inlinegrouptabular"] input[name*="DELETE"]').hide();
    $('div[name="inlinegrouptabular"] a.deletelink').bind("click", function(){
        $(this).prev('input').attr('checked', !$(this).prev('input').attr('checked'));
        delete_item = $(this).parent().parent().parent().parent().parent(); // tbody
        if (delete_item.hasClass('item')) {
            // append to end of table
            new_item = delete_item.clone(true).appendTo(delete_item.parent());
        } else {
            // insertAfter last item (before the first predelete-item)
            new_item = delete_item.clone(true).insertAfter(delete_item.parent().find('tbody.item:last'));
        }
        new_item.toggleClass('item');
        new_item.toggleClass('predelete-item');
        delete_item.remove(); // important: remove before insertAfter
    });
    
    function Hinweis () {
        alert("xxx");
    };
    
    /// DRAG & DROP
    $('div[name="inlinegrouptabular"].sortable').sortable({
        axis: 'y',
        items: 'tbody.item',
        handle: '.draghandler',
        placeholder: 'placeholder',
        tolerance: 'intersect',
        containment: 'table',
        start: function(e, ui) {
            temp_html = ""
            ui.item.find('tr:last td').each(function() {
               temp_html += "<td></td>" 
            });
            $('tbody.placeholder').html("<tr>" + temp_html + "</tr>");
        },
        //forcePlacehholderSize: true,
        helper: function(e, el) {
            $("div.sortablehelper").find('h2:first').text(el.find('p:first').text());
            return $("div.sortablehelper")
                .clone()
                .width(el.width() + 'px');
        },
        update: function(e, ui) {
            /// remove display:block, generated by UI sortable
            $(this).removeAttr('style');
        }
    });
    
    // set ORDER_FIELDS on submit
    $("form").submit(function() {
        $('div[name="inlinegrouptabular"].sortable').each(function() {
            counter = 0;
            predelete_counter = $(this).find('tbody').length - $(this).find('input[name*="DELETE"]:checked').length;;
            $(this).find('tbody').each(function(i) {
                input_values = "";
                fields = $(this).find(':input:not([name*="order"])').serializeArray();
                $.each(fields, function(i, field) {
                    input_values += field.value;
                });
                predelete_flag = $(this).find('input[name*="DELETE"]:checked').length;
                if (input_values == "") {
                    /// clear order-field for empty items
                    $(this).find('input[id*="order"]').val('');
                } else if (predelete_flag) {
                    /// reset order-field for predelete-item
                    $(this).find('input[id*="order"]').val(predelete_counter);
                    predelete_counter = predelete_counter + 1;
                } else {
                    /// reset order-field
                    $(this).find('input[id*="order"]').val(counter);
                    counter = counter + 1;
                }
            });
        });
    });
    
    
    
});



