$(document).ready(
	function(){
		var sigue = false;
		$('#nextbtn').click(function(){
			var text = $("#debTitleForm").val()
			// $("#titulodebform").text(text)
			document.getElementById("titulodebform1").innerHTML = text;
			document.getElementById("titulodebform2").innerHTML = text;
		});
		$("#debTitleForm").on("keyup", function(){
		    if($(this).val() != "" && $("#debTextForm").val() != ""){
		        sigue = true;
		    } else {
						sigue = false;
		    }
		});

		$("#debTextForm").on("keyup", function(){
		    if($(this).val() != "" && $("#debTitleForm").val() != ""){
		        sigue = true;

		    } else {
		        sigue = false;
		    }});
		$('#userOrderTypeForm').on('change', function() {
			order_user_by(this.value);
		});
		$('#debMemberTypeForm').on('change', function() {
			if (this.value == 1){
				document.getElementById('usuariosPrivado_modal').style.display="block";
				document.getElementById('modificarusr').style.display="block";
				document.getElementById('moficarlista').style.display="None";
				document.getElementById('usuariosPrivadoLista_modal').style.display="None";
			}
			else if (this.value == 2) {
				document.getElementById('usuariosPrivadoLista_modal').style.display="block";
				document.getElementById('moficarlista').style.display="block";
				document.getElementById('modificarusr').style.display="None";
				document.getElementById('usuariosPrivado_modal').style.display="None";
			}
			else{
				document.getElementById('modificarusr').style.display="None";
				document.getElementById('moficarlista').style.display="None";
				document.getElementById('usuariosPrivado_modal').style.display="None";
				document.getElementById('usuariosPrivadoLista_modal').style.display="None";
			}
		});
		//jQuery time
		var current_fs, next_fs, previous_fs; //fieldsets
		var left, opacity, scale; //fieldset properties which we will animate
		var animating; //flag to prevent quick multi-click glitches
		$(".next").click(function(){
			if (sigue){
				if(animating) return false;
				animating = true;

				current_fs = $(this).parent();
				next_fs = $(this).parent().next();


				//activate next step on progressbar using the index of next_fs
				$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

				//show the next fieldset
				next_fs.show();
				//hide the current fieldset with style
				current_fs.animate({opacity: 0}, {
					step: function(now, mx) {
						//as the opacity of current_fs reduces to 0 - stored in "now"
						//1. scale current_fs down to 80%
						scale = 1 - (1 - now) * 0.2;
						//2. bring next_fs from the right(50%)
						left = (now * 50)+"%";
						//3. increase opacity of next_fs to 1 as it moves in
						opacity = 1 - now;
						current_fs.css({
			        'transform': 'scale('+scale+')',
			        'position': 'absolute'
			      });
						next_fs.css({'left': left, 'opacity': opacity});
					},
					duration: 800,
					complete: function(){
						current_fs.hide();
						animating = false;
					},
					//this comes from the custom easing plugin
					// easing: 'easeInOutBack'
				});
			}
			else {
				if ($("#debTitleForm").val() == ""){
					$("#errorTitulo").css("display","block");
				}
				else {
					$("#errorTitulo").css("display","none");
				}
				if ($("#debTextForm").val() == ""){
					$("#errorDesc").css("display","block");
				}
				else {
					$("#errorTitulo").css("display","none");
				}
			}
		});

		$(".previous").click(function(){
			if(animating) return false;
			animating = true;

			current_fs = $(this).parent();
			previous_fs = $(this).parent().prev();

			//de-activate current step on progressbar
			$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

			//show the previous fieldset
			previous_fs.show();
			//hide the current fieldset with style
			current_fs.animate({opacity: 0}, {
				step: function(now, mx) {
					//as the opacity of current_fs reduces to 0 - stored in "now"
					//1. scale previous_fs from 80% to 100%
					scale = 0.8 + (1 - now) * 0.2;
					//2. take current_fs to the right(50%) - from 0%
					left = ((1-now) * 50)+"%";
					//3. increase opacity of previous_fs to 1 as it moves in
					opacity = 1 - now;
					current_fs.css({'left': left});
					previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity, 'position': 'relative'});
				},
				duration: 800,
				complete: function(){
					current_fs.hide();
					animating = false;
				},
				//this comes from the custom easing plugin
				// easing: 'easeInOutBack'
			});
		});

	});

$(document).ready(function(){
	filtroCheckbox('#searchUser1');
	filtroCheckbox('#searchLista1');
});

function order_user_by(value){
	$.ajax({
			url:  $(this).attr("href"),
			type: 'GET',
			data:{  order : value,
							csrfmiddlewaretoken: '{{ csrf_token }}'
						} ,
						success: function(data) {
							var container = $('#containercheckbox');
							var inputs = container.find('div');
							var id = inputs.length+1;
							inputs.remove()
							for (i=0 ; i<data.length ; i++){
								var name = " "+data[i].name
								var value = JSON.stringify(data[i].object);
								var div = $('<div />', {class:"inputGroup"});
								var label = $('<label />', { 'for': 'debMembersForm_'+i, text: name});
								var input = $('<input />', { type: 'checkbox', name:"members", value: value, id: 'debMembersForm_'+i})

								input.prependTo(label.appendTo(div.appendTo(container)));
							}
						},
						failure: function(data) {
								alert('Error de conexión');
						},
						crossDomain: true
				});
 }

 $(window).load(function(){

  $(function() {
   $('#debImgForm').change(function(e) {
       addImage(e);
      });

      function addImage(e){
       var file = e.target.files[0],
       imageType = /image.*/;

       if (!file.type.match(imageType))
        return;

       var reader = new FileReader();
       reader.onload = fileOnload;
       reader.readAsDataURL(file);
      }

      function fileOnload(e) {
       var result=e.target.result;
       $('#imgPrev').attr("src",result);
      }
     });
   });
