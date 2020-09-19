var $ = jQuery.noConflict();

$('.message a').click(function(){
   $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
});


$("#eliminarP").on('click', function() {
     alert("Has dado Click");

});

function abrirmodaleliminar(url)
{
     $('#eliminar').load(url, function()
          {
           $(this).modal({
                backdrop: 'static',
                keyboard: false
            })


               $(this).modal('show');
            });
}