function AdBehavior(element) {
    // 'element' should be a jQuery object
    this.id = element.attr('id').split('.')[1]; // Numerical 'ID' of this element
    
    // Elements
    this.select_el = element;
    this.impression_el = $('input[@id="id_scheduledad.' + this.id + '.impression_limit"]').parent();
    this.clickthrough_el = $('input[@id="id_scheduledad.' + this.id + '.clickthrough_limit"]').parent();
    this.date_el = $('input[@id="id_scheduledad.' + this.id + '.end_date_date"]').parent().parent();
    
    this.select_el.bind('change', {behavior: this},
        function(event){
            event.data.behavior.toggle_els();
    });
    
    this.hide_all(true);    // Abruptly hides all elements
    this.toggle_els();      // Shows the proper element with transition
}

AdBehavior.prototype.do_effect = function(element, type, speed){
    // 'element' must be a jQuery object   
    if (type == 'show' || type == 'hide') {
        element.animate({height: type, opacity: type}, speed);
        return true;
    } else {
        return false;
    }
};

AdBehavior.prototype.hide_all = function(abrupt) {
    if (abrupt){    // If 'abrupt=true' then we have to hide all elements instantaneously
        this.impression_el.hide();
        this.clickthrough_el.hide();
        this.date_el.hide();
        
        return true;

    } else if (!abrupt) {   // Hide all visible elements with transition
        if (this.impression_el.css('display') != 'none')
            this.do_effect(this.impression_el, 'hide');

        if (this.clickthrough_el.css('display') != 'none')
            this.do_effect(this.clickthrough_el, 'hide');

        if (this.date_el.css('display') != 'none')
            this.do_effect(this.date_el, 'hide');

        return true;
    }
    
    return false;
};

AdBehavior.prototype.toggle_els = function (speed){
    if (!speed){speed='slow';}

    this.hide_all();    // Hide all elements first
    
    switch (this.select_el.val()) {
        case '0':
            this.hide_all(true);
            break
        case '1':
            this.do_effect(this.date_el, 'show', speed)
            break
        case '2':
            this.do_effect(this.impression_el, 'show', speed)
            break
        case '3':
            this.do_effect(this.clickthrough_el, 'show', speed)
            break
    }
};


$(document).ready(function(){
    ELEMENTS = $('select[@id$=".behavior"]');
    for (var i=0; i < ELEMENTS.length; i++){
        adbehavior = new AdBehavior($(ELEMENTS[i]));
    }
});