//  This is VERY messy and needs to be fixed in order to be much leaner and efficient...

//left = 800;  // Over-ride the width of the main content div

function buildAllowableAdTypesList(el){
    var returnString = '';
    for (var i = 0; i < el.options.length; i++){
        if (el.options[i].selected)
            returnString += '<li>' + el.options[i].text + '</li>';
    }
    return returnString;
};

function buildPlacementInterface(){    
    //  Resize the main content div
    content_box = $('div#content');
    //content_box.removeClass('colMS').addClass('colM');
    
    if ($('div#content h1:contains("Change")')){
        var box = $('<div class="form-row"></div>');
        box.insertBefore($('select[@id="id_allowable_ad_types"]').parent());
        
        var allowable_ad_types = $('select[@id="id_allowable_ad_types"]');
        var image_field = $('input[@id="id_image_file"]');
        var image_link = image_field.parent().children().filter('a');    // This may not exist
        var height = $('input[@id="id_height"]');
        var width = $('input[@id="id_width"]');

        if (image_link.length > 0) {
            allowable_ad_types.parent().hide();
            image_field.parent().hide();
            height.parent().hide();
            width.parent().hide()
            
            image_url = image_link.html().split(' ');
            image_url = image_url[1];
            
            var htmlToInsert = '<p style="float: right; margin-right: 550px;"><a class="thickbox" title="Sample Placement location" href="http://media.dailybruin.com/dailybruin/' + image_url + '">';
            htmlToInsert += '<img style="border: 1px solid black;" height="150px" alt="Placement" src="http://media.dailybruin.com/dailybruin/' + image_url + '" /></a>';
            htmlToInsert += '<h3>Allowable Ad Types</h3><ul style="margin-left:0;">' + buildAllowableAdTypesList(allowable_ad_types[0]) + '</ul>';
            htmlToInsert += '<h3>Size Restrictions</h3><ul style="margin-left:0;"><li>Height: ' + height.val() + 'px</li><li>Width: ' + width.val() + 'px</li></ul>';
            htmlToInsert += '</p>';
            box.html(htmlToInsert);

            tb_init('a.thickbox, area.thickbox, input.thickbox');
        }
    }
};

function checkPlacementType(el, els){
        if (el.val() == 2){ // Multi Ad
            for (var i=0; i < els.length; i++)
                els[i].show();
        } else {
            for (var i=0; i < els.length; i++)
                els[i].hide();
        }
};

function bindPlacementType(selectElement){
    var numAds = $('input[@id="id_num_ads"]').parent();
    var orientation = $('select[@id="id_orientation"]').parent();
    var orderthese = $('ul#orderthese');
    
    checkPlacementType($(selectElement[0]), [numAds, orientation, orderthese]);
    
    $(selectElement[0]).bind('change', {numAds: numAds, orientation: orientation, orderthese: orderthese}, function(event){
        checkPlacementType($(this), [event.data.numAds, event.data.orientation, event.data.orderthese]);
    });
};

addEvent(window, 'load', buildPlacementInterface);

$(document).ready(function(){
    bindPlacementType( $('select[@id="id_type_placement"]'))
});