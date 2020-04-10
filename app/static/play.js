$(document).ready(function(){
    loadState();
});

window.refresh = function(data){
    window.location.href = data.url;
}

function loadState() {
    window.setTimeout(function(){
        $.ajax({
            url: '/long_polling',
            method: 'GET',
            dataType: 'json',
            success: function(event){
                    window['refresh'](event);
                    loadState();
            }
        });
    }, 2000);
}
