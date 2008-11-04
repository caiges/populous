window.onload = function(){
    div = document.getElementById('content-main');
    type = div.parentNode.childNodes[1].innerHTML.split('Add' )[1];
    container = document.createElement('div');
    container.setAttribute('id', 'content-related');
    container.setAttribute('style', 'float: right; margin-left: 800px; position: fixed; width: 300px;');
    container.innerHTML = '<div class="module" id="recent-actions-module"><h2>Ads by this client</h2><h3>Recent Ads</h3><ul id="client_ad_list"><li>None available</li></ul></div>';
    div.parentNode.insertBefore(container, div.nextSibling);
    
    client_id = window.location.toString().split('/');
    client_id = client_id[client_id.length-2];
    
    ul_el = $('ul#client_ad_list');
    ul_el.html('<li>loading</li');
    ul_el.load('/admin/client_lookup/', {client_id: client_id});
};