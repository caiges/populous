// fetch var APP_URLS
var APP_URLS;
APP_URLS = {16: '../../../admin/log/',347: '../../../advertisements/baseads/',351: '../../../advertisements/coupons/',346: '../../../advertisements/couponcategories/',349: '../../../advertisements/graphicads/',348: '../../../advertisements/textads/',350: '../../../advertisements/videoads/',342: '../../../advertising/clients/',343: '../../../advertising/placements/',345: '../../../advertising/scheduledads/',344: '../../../advertising/statistics/',18: '../../../alerts/lists/',20: '../../../alerts/subscriptions/',19: '../../../alerts/types/',21: '../../../alerts/archivedalerts/',6: '../../../auth/groups/',8: '../../../auth/messages/',5: '../../../auth/permissions/',7: '../../../auth/users/',268: '../../../banners/banners/',131: '../../../births/births/',132: '../../../births/children/',24: '../../../blogs/authors/',23: '../../../blogs/blogs/',22: '../../../blogs/collections/',27: '../../../blogs/blogrolls/',25: '../../../blogs/entries/',26: '../../../blogs/quicklinks/',28: '../../../categories/categories/',229: '../../../classifieds/ads/',227: '../../../classifieds/categorys/',228: '../../../classifieds/subcategorys/',11: '../../../comments/comments/',12: '../../../comments/freecomments/',13: '../../../comments/karma/',15: '../../../comments/moderatordeletions/',14: '../../../comments/userflags/',307: '../../../configuration/dbtvs/',310: '../../../configuration/dbtvboxs/',309: '../../../configuration/frontpages/',311: '../../../configuration/topstoriess/',308: '../../../configuration/vids/',3: '../../../core/contenttypes/',2: '../../../core/packages/',4: '../../../core/sessions/',1: '../../../core/sites/',36: '../../../drinkspecials/drinkspecials/',49: '../../../events/events/',48: '../../../events/eventcategories/',50: '../../../events/eventtimes/',51: '../../../events/recurringeventtimes/',53: '../../../events/recurringreminders/',52: '../../../events/reminders/',54: '../../../events/usersubmittedevents/',9: '../../../flatpages/flatpages/',55: '../../../fragments/fragments/',313: '../../../legacy/legacyobjects/',56: '../../../mailform/mailform/',57: '../../../mailfriend/maileditems/',60: '../../../media/photos/',312: '../../../media/printeditions/',62: '../../../media/secondaryvideos/',61: '../../../media/videos/',267: '../../../merchants/hourss/',266: '../../../merchants/stores/',63: '../../../movies/movies/',64: '../../../movies/movieshowings/',42: '../../../music/albums/',44: '../../../music/albumsongs/',46: '../../../music/audiointerviews/',39: '../../../music/bands/',40: '../../../music/instruments/',37: '../../../music/musicgenres/',38: '../../../music/musicians/',41: '../../../music/musiciansinbands/',43: '../../../music/songs/',45: '../../../music/songranks/',47: '../../../music/stationids/',69: '../../../news/combinedsections/',70: '../../../news/combinedsectionpieces/',65: '../../../news/datelines/',74: '../../../news/framings/',75: '../../../news/recurringinlines/',273: '../../../news/relatedtoptopics/',67: '../../../news/sections/',71: '../../../news/sectionpriorities/',68: '../../../news/sectionrules/',72: '../../../news/staticsections/',73: '../../../news/staticsectionstories/',66: '../../../news/stories/',76: '../../../news/story_inline_mapping/',271: '../../../news/topics/',269: '../../../news/topicss/',272: '../../../news/toptopics/',78: '../../../onthestreet/featuredanswers/',77: '../../../onthestreet/questions/',254: '../../../parking/parkinglocations/',253: '../../../parking/prices/',80: '../../../persistentsearch/results_seen/',79: '../../../persistentsearch/searches/',130: '../../../photogalleries/galleryphotos/',128: '../../../photogalleries/gallerysets/',129: '../../../photogalleries/galleries/',34: '../../../places/businesshours/',29: '../../../places/cities/',30: '../../../places/counties/',35: '../../../places/kitchenhours/',31: '../../../places/neighborhoods/',33: '../../../places/places/',32: '../../../places/placetypes/',81: '../../../playlists/playlists/',82: '../../../playlists/playlistsongs/',84: '../../../podcasts/episodes/',83: '../../../podcasts/shows/',86: '../../../polls/choices/',88: '../../../polls/combinedchoices/',87: '../../../polls/combinedpolls/',85: '../../../polls/polls/',302: '../../../publications/categorys/',303: '../../../publications/entrys/',90: '../../../q_and_a/questions/',89: '../../../q_and_a/questionsets/',93: '../../../questionaire/answers/',92: '../../../questionaire/answersets/',95: '../../../questionaire/completed_questionaires/',94: '../../../questionaire/questions/',91: '../../../questionaire/questionaires/',96: '../../../questionaire/questionaire_responses/',99: '../../../quizzes/contestants/',100: '../../../quizzes/answers/',98: '../../../quizzes/questions/',97: '../../../quizzes/quizzes/',101: '../../../recipes/recipes/',102: '../../../recipes/recipeingredients/',10: '../../../redirects/redirects/',103: '../../../registration/challenges/',104: '../../../registration/privatemessages/',105: '../../../relatedlinks/relatedlinks/',237: '../../../restaurants/cuisines/',238: '../../../restaurants/restaurants/',110: '../../../search/links/',109: '../../../search/words/',108: '../../../search/wordlists/',111: '../../../sexoffenders/cities/',112: '../../../sexoffenders/schools/',113: '../../../sexoffenders/sexoffenders/',17: '../../../sms/providers/',125: '../../../society/couples/',126: '../../../society/couple_events/',127: '../../../society/obits/',292: '../../../sports/schools/',293: '../../../sports/scores/',291: '../../../sports/sports/',59: '../../../staff/positions/',58: '../../../staff/staffmembers/',114: '../../../throttle/throttle/',123: '../../../weather/alert_event_types/',115: '../../../weather/conditions/',116: '../../../weather/dayforecasts/',117: '../../../weather/textforecasts/',122: '../../../weather/forecast_zones/',121: '../../../weather/images/',120: '../../../weather/imagetypes/',124: '../../../weather/alerts/',119: '../../../weather/severe_weather_alerts/',118: '../../../weather/sunmoon/'};$.getScript("/admin/generic_urls.js", function(){
$(document).ready(function(){
        alignFields();
        parse_relations();	// Start working!
    });
});

function alignFields (){
    id_els  = $('input[@id$=".ad_id"]');
    type_els = $('a[@id$=".ad_type"]');
    for (var i = 0; i < id_els.length; i++){
        $(type_els[i]).after($(id_els[i]).parent().html());
        $(id_els[i]).parent().remove()
    }
};

function dismissRelatedLookupPopup(win, chosenId) {
    var elem = document.getElementById(win.name);
    if (elem.className.indexOf('vRawIdAdminField') != -1 && elem.value) {
        elem.value += ',' + chosenId;
    } else {
        document.getElementById(win.name).value = chosenId;
    }
    win.close();
    setTimeout(function(){$(elem).trigger('change')}, 1)
}

function GenericRelation (contenttype_select, objectid_input) {
    this.contenttype_select = contenttype_select;   // jQuery element of the 'select' field
    this.objectid_input = objectid_input;           // jQuery element of the 'input' field

    this.lookup_el;     // Will be defined later
    this.container;
    this.display_field = this.create_display_field();   // jQuery element to show 'objectid' display info (returned from server)
    this.python_module_name = this.get_python_module_name();    // String containing 'python_module_name'
}

GenericRelation.prototype.create_display_field = function () {
    // Creates a lookup link and icon as well as a text field for displaying results of xmlhttp lookup.
    // HIDDEN on creation

    container = $('<div class="related_content_wrapper"></div>');
    container.appendTo(this.objectid_input.parent());
    container.css({width: '150px', display: 'inline'});
    container.hide();

    lookup_el = $('<a href="" accesskey="101"><img width="16" height="16" alt="Lookup" src="http://media.dailybruin.com/admin_media/img/admin/selector-search.gif"/></a>');

    lookup_el.attr({ 'id': 'lookup_' + this.objectid_input.attr('id'), 'href': APP_URLS[this.contenttype_select.val()], 'class': 'related-lookup', 'onclick': 'return showRelatedObjectLookupPopup(this);' });
    lookup_el.appendTo(container);
    
    text_el = $("<strong id='" + this.objectid_input.attr('id') + "_text'></strong>");
    text_el.appendTo(container);
    
    // Assign variables
    this.lookup_el = lookup_el;
    this.container = container;
    return text_el;
};

GenericRelation.prototype.get_python_module_name = function () {
    id = this.contenttype_select.attr('id');
    return id.split('.')[0].split('_')[1];	//Takes care of both possible senarios
};

GenericRelation.prototype.set_lookup = function () {
    if (this.contenttype_select.val()) {
        this.lookup_el.attr('href', APP_URLS[this.contenttype_select.val()]);
        this.container.css('display', 'inline');
    } else {
        this.container.css('display', 'none');
    }
};

GenericRelation.prototype.do_lookup = function () {
    // Calls the server and returns the data
    this.display_field.html('loading');    
    this.display_field.load("/admin/generic_lookup/", {content_type_id: this.contenttype_select.val(), object_id: this.objectid_input.val(), limit: 10});
};

function parse_relations(){
    var RELATION_ELEMENTS = {'content_types': $('select[@id$="_type"]'), 'object_ids': $('input[@id$="_id"]')};    
    
    if (RELATION_ELEMENTS['content_types'].length != RELATION_ELEMENTS['object_ids'].length){
        //alert("Error:\n\n" + "RELATION_ELEMENTS['content_types'].length != RELATION_ELEMENTS['object_ids'].length")

    } else {
        for (var i=0; i < RELATION_ELEMENTS['content_types'].length; i++){
            contenttype_select = $(RELATION_ELEMENTS['content_types'][i]);
            objectid_input = $(RELATION_ELEMENTS['object_ids'][i]);
            relation = new GenericRelation(contenttype_select, objectid_input);

            // Attach events
            objectid_input.bind('change', {relation: relation},
            function(event){
                event.data.relation.do_lookup();
            });
            contenttype_select.bind('change', {relation: relation},
                function(event){
                    event.data.relation.set_lookup();
            });
            
            
            // Run if there are default values
            if (objectid_input.val()){
            	relation.do_lookup();
                relation.set_lookup();
            }
        }
    }
};