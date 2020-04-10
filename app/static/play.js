$(document).ready(function(){
    loadState();
});


function loadState() {
    window.setTimeout(function(){
        $.ajax({
            url: '/long_polling',
            method: 'GET',
            dataType: 'json',
            success: function(event){
                # manipulate elements
                loadState();
            }
        });
    }, 2000);
}
