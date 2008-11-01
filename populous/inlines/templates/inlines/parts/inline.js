{
    name: "{{ inline.name }}",
    className: "{{ inline.class_name }}",
    beforeInsert: function(h) {
        var data;
        $.get("{{ inline.get_form_url }}", function(html) {
                inline_box.show();
                $("#inline-content h1").text("Add Inline: " + h.name);
                $("#inline-content div").html(html);
        });
    }
}