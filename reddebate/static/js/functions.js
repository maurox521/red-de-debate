$(function() {
  $('a[href="#search"]').on("click", function(event) {
    event.preventDefault();
    $("#search").addClass("open");
    $('#search > form > input[type="search"]').focus();
  });

  $("#search, #search button.close").on("click keyup", function(event) {
    if (
      event.target == this ||
      event.target.className == "close" ||
      event.keyCode == 27
    ) {
      $(this).removeClass("open");
    }
  });
});

function form_perfil(boton, form){
  document.getElementById(boton).style.display = 'none';
  document.getElementById(form).style.display = 'block';
}

function cancelar_form(boton, form){
  document.getElementById(form).style.display = 'none';
  document.getElementById(boton).style.display = 'inline-block';
  $('#'+form+' :input').each(function() {
    $(this).val('');
  });
}

function fomulario_argumento(position){
  document.getElementById('bot_argumento'+position).style.display = 'none';
  document.getElementById('form_argumento'+position).style.display = 'block';
}

function despliega_formulario(id){
  $(id).slideDown("slow");
  $('html, body').animate({scrollTop : 0},800);
  $(nuevoDebateBtn).hide();
};
function confirm_modal_show(id, deb, title) {
  $("#fechafin2").hide();
  $(".modalcontainerconfirm").fadeIn("slow");
  if (id==1){
    $("#cerrarDebate").fadeIn("slow");
    $("#iddebacerrar").val(deb);
    $("#titulodebcerrar").text(title);
  }
  else{
    $("#republicarDebate").fadeIn("slow");
    $("#iddebarepublicar").val(deb);
    $("#titulodebrepublicar").text(title);
  }
};
function confirm_modal_close() {
  $(".modalcontainerconfirm").fadeOut("slow");
  $(".modalconfirm").fadeOut("slow");
};
function cierra_formulario(id){
  $(id).slideUp("slow");
  $(nuevoDebateBtn).show();
}
function toggle_div(id){
  $(id).slideToggle();
}
function formulario_editar_debate(id,id_dbt,title,desc,año,mes,dia,alias,length){
  $(id).slideDown("slow");
  $("html, body").animate({ scrollTop: 0 }, 600);
  document.getElementById('tituloeditar').value = title;
  document.getElementById('desceditar').value = desc;
  document.getElementById('iddbteditar').value = id_dbt;

  date=año+"-"+mes+"-"+dia
  if (date!="--"){
    document.getElementById('fechaeditar').value = date; }
  else{
    document.getElementById('fechaeditar').value = null; }
  if (alias=="username"){
    document.getElementById('radio4e').checked= true; }
  else{
    document.getElementById('radio5e').checked= true; }
  if(length==300){
    document.getElementById('radio1e').checked= true; }
  else if (length==200){
    document.getElementById('radio2e').checked= true; }
  else{
    document.getElementById('radio3e').checked= true; }
}

function filtrar_debate(myinput,tabla) {
  var input, filter, table, tr, td, i;
  input = document.getElementById(myinput);
  filter = input.value.toUpperCase();
  table = document.getElementById(tabla);
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[2];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = ""; }
      else {
        tr[i].style.display = "none"; }
    }
  }
}

function debate_estado(evt, estadoDbt) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none"; }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", ""); }
  document.getElementById(estadoDbt).style.display = "block";
  evt.currentTarget.className += " active";
}


function abrir_modal(modal){
  document.getElementById(modal).style.display="block";
}

function cerrar_modal(modal){
  document.getElementById(modal).style.display="none";
}

function definir_postura(id_debate, position, post_f, post_c){
  if (document.getElementById('argumentos')){
    $("#argumentos").slideDown("slow");
  }
  cambiar_postura(id_debate, position, post_f, post_c);
}
function confirmar_cambio(post) {
   document.getElementById("cambioPostura_modal").style.display="block";
   document.getElementById("postura_debate").value = post;
}

function ver(evt, estadoDbt) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none"; }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", ""); }
  document.getElementById(estadoDbt).style.display = "block";
  evt.currentTarget.className += " active";
}

function borrarFecha(){
  $('#debEndDateForm').val("")
}

function spinnerReglas(id, operacion, max, min, paso){
  var valor = $('#'+id).val();
  if(operacion>0){
    if(parseInt(valor) < parseInt(max)){
      $('#'+id).val(parseInt(valor)+parseInt(paso));
    }
  }
  else {
    if(parseInt(valor) > parseInt(min)){
      $('#'+id).val(parseInt(valor)-parseInt(paso));
    }
  }

}
function cortarTexto(texto){
  var limite = 100;
  if(texto.length > limite)
  {
    texto = texto.substring(0,limite) + "...";
  }

    document.write(texto);
}

function creartags(){
  var texto = $("#debTitleForm").val();
  var res = texto.split(" ");
  console.log(res);

};

function mostrarFecha(){
  document.getElementById("fechafin2").disabled = false;
  $("#fechafin2").show();
  var date = new Date()
  dd = date.getDate();
  mm = date.getMonth() + 1;
  yyyy = date.getFullYear()
  if (dd<10){dd='0'+dd};
  if (mm<10){mm='0'+mm};
  $("#fechafin2").val(yyyy+'-'+mm+'-'+dd)
}
function quitarFecha(){
  document.getElementById("fechafin2").disabled = true;
  $("#fechafin2").hide();
}

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}
function filtroCheckbox(id){
  $(id).on("input",function(){

      var searchTxt = $(this).val();
      searchTxt = searchTxt.replace(/[.()+]/g,"\\$&");
      var patt = new RegExp("^" + searchTxt,"i");
      $(":checkbox").each(function(){
          var label = $(this).parent().text().trim();
          if(patt.test(label)){
            $(this).closest("div").show();
            console.log(label);
          }
          else{
            $(this).closest("div").hide();
          }


      })
  });
};
function filtroPanel(id){
  $(id).on("input",function(){

      var searchTxt = $(this).val();
      searchTxt = searchTxt.replace(/[.()+]/g,"\\$&");
      var patt = new RegExp("^" + searchTxt,"i");
      $(".dummy-media-object").each(function(){
          var label = $(this).text().trim();
          console.log(label);
          if(patt.test(label)){
            $(this).closest("a").show();
            console.log(label);
          }
          else{
            $(this).closest("a").hide();
          }


      })
  });
};
// Gráficos

function posturaChart() {
  var data = google.visualization.arrayToDataTable([
          ['Position', 'Cantidad'],
          ['A Favor', varGlobal.infavor_position],
          ['En Contra', varGlobal.against_position]
        ]);

        var options = {
          title: 'Resumen Posturas',
          width:400,
          height:300,
          colors: ['#18BD9B', '#d9534f'],
          backgroundColor: { fill: "transparent" }
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_postura'));
        google.visualization.events.addListener(chart, 'ready', function () {
            var imgUri = chart.getImageURI();
            // do something with the image URI, like:
            document.getElementById('chartImg').src = imgUri;
        });
        chart.draw(data, options);

};
function argumentosChart() {
  var data = google.visualization.arrayToDataTable([
          ['Argumentos', 'Cantidad'],
          ['A Favor', varGlobal.args_infavor],
          ['En Contra', varGlobal.args_against]
        ]);

        var options = {
          title: 'Resumen Argumentos',
          width:400,
          height:300,
          colors: ['#18BD9B', '#d9534f'],
          backgroundColor: { fill: "transparent" }
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_argumento'));
        chart.draw(data, options);
};

function cambioPosturaChart() {
  var data = google.visualization.arrayToDataTable([
          ['Cambio', 'Cantidad'],
          ['De Favor a Contra', varGlobal.infavor_to_against],
          ['De Contra a Favor', varGlobal.against_to_infavor]
        ]);
        var title = 'Usuarios que cambiaron de posición: '+varGlobal.position_change;
        if (owner_id === actual_id){
          var title = title+'\n Haz clic para ver detalles';
        }
        var options = {
          title: title,
          width:400,
          height:300,
          colors: ['#d9534f','#18BD9B'],
          backgroundColor: { fill: "transparent" }
        };

        try {
          var chart = new google.visualization.PieChart(document.getElementById('piechart_cambioPostura'));
          if (owner_id === actual_id){
            google.visualization.events.addListener(chart, 'select', function () {
                abrir_modal('positionChange_modal');
            });
          }
          chart.draw(data, options);
        } catch (e) {
          console.log(e);
        }
};

// function mejorArgumentoChart(){
//   var data = new google.visualization.arrayToDataTable([
//       ['Valoración', 'A Favor','En Contra'],
//       ['1º Mejor Valorado', varGlobal.primer_arg_f  ,varGlobal.primer_arg_c],
//       ['2º Mejor Valorado', varGlobal.segundo_arg_f  , varGlobal.segundo_arg_c]]);
//     var options = {
//       title: 'Argumentos a favor y en contra más valorados',
//       chartArea: {width: '50%'},
//       bars: 'horizontal', // Required for Material Bar Charts.
//       backgroundColor: { fill: "transparent" },
//       series: {
//         0: { color: '18BD9B'}, // Bind series 0 to an axis named 'distance'.
//         1: { color: 'd9534f'} // Bind series 1 to an axis named 'brightness'.
//       },
//       hAxis: {
//           title: 'Cantidad'
//         },
//         vAxis: {
//           title: 'Valoración'
//         }
//     };
//     var chart = new google.visualization.BarChart(document.getElementById('chart_mejorArgumento'));
//     chart.draw(data, options);
//    };
function razonCambioChart(){
  var data = new google.visualization.arrayToDataTable([
      ['Razón', 'De Favor a Contra','De Contra a Favor'],
      ['Cambió de opinión', varGlobal.reason_infavor_to_against[0]  ,varGlobal.reason_against_to_infavor[0]],
      ['Error de clic', varGlobal.reason_infavor_to_against[1]  ,varGlobal.reason_against_to_infavor[1]],
      ['Otro', varGlobal.reason_infavor_to_against[2] , varGlobal.reason_against_to_infavor[2]]]);
      var div_width = document.getElementById("chart_razonCambio").offsetWidth;
      if (owner_id === actual_id){
        area_width = 400;
        div_width = 800;
      }
      else{
        area_width = div_width*0.5;
        div_width = div_width;
      }
      var options = {
        title: 'Motivos cambio de posición',
        chartArea: {width:area_width },
        width: div_width,
        isStacked: true,
        backgroundColor: { fill: "transparent" },
        series: {
          0: { color: 'd9534f'}, // Bind series 0 to an axis named 'distance'.
          1: { color: '18BD9B'} // Bind series 1 to an axis named 'brightness'.
        },
        hAxis: {
          title: 'Cantidad',
          minValue: 0,
          format: '0',
        },
        vAxis: {
          title: 'Motivos'
        }
      };
      var chart = new google.visualization.BarChart(document.getElementById('chart_razonCambio'));
      chart.draw(data, options);
    };
  function posturasTiempo() {
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Fecha');
    data.addColumn('number', 'Posturas');
    for (i=0 ; i<positions_by_day.length ; i++){
      var date = positions_by_day[i][0].split("-")
      var value = positions_by_day[i][1];
      data.addRow([new Date(parseInt(date[0]),parseInt(date[1])-1,parseInt(date[2])), value]);
    };
    var chart = new google.visualization.AnnotationChart(document.getElementById('chart_div'));

    var options = {
      displayAnnotations: true,
      colors: ['#2D3E50'],
      width: document.getElementById("stats_div").offsetWidth*0.95,
    };

    chart.draw(data, options);
  };
$(function() {
 $('#updateDebImgForm').change(function(e) {
     updateImage(e);
     console.log("UPDATE");
    });

    function updateImage(e){
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
     $('#updateImgPrev').attr("src",result);
    }
   });
