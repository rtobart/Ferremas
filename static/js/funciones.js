// FUNCION/VALIDACION LOGIN (CON CORREO)
var expr = /^[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+$/;
$(document).ready(function() {
$("#enviar").click(function() {
    var email = $("#email").val();
    var pass = $("#pass").val();

    if (email === "" || !expr.test(email)) {
    $("#mensaje1").fadeIn();
    return false;
    } else {
    $("#mensaje1").fadeOut();
    }
    
    if (pass === "") {
    $("#mensaje2").fadeIn();
    return false;
    } else {
    $("#mensaje2").fadeOut();
    }
});
});

// FUNCION/VALIDACION REGISTRO
var expr = /^[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]+$/;
var nombre = document.getElementById('nombre');
var apellido = document.getElementById('apellido');
var email = document.getElementById('email');
var pass = document.getElementById('pass');
var error = document.getElementById('error');
//error.style.color='red';

function enviarFormulario() {
    console.log('Enviando formulario...');
    var mensajeError =[];
    if(nombre.value===null||nombre.value==='') {
        $("#mensaje1").fadeIn();
        return false;
    } else {
        $("#mensaje1").fadeOut();
    }

    if(apellido.value===null||apellido.value==='') {
        $("#mensaje2").fadeIn();
        return false;
    } else {
        $("#mensaje2").fadeOut();
    }

    if(email.value===null||email.value===''||!expr.test(email)) {
        $("#mensaje3").fadeIn();
        return false;
    } else {
        $("#mensaje3").fadeOut();
    }

    if(pass.value===null||pass.value==='') {
        $("#mensaje4").fadeIn();
        return false;
    } else {
        $("#mensaje4").fadeOut();
    }
    //error.innerHTML=mensajeError.join(' - ');
    return false;
}
function formu() {
    alert('¡Un Administrador recibirá la información!');
}

function NumAleatorio() {
var numero = Math.floor(Math.random() * 100) + 1;
var resultadoElemento = document.getElementById('resultado');

if (numero <= 33) {
    resultadoElemento.innerHTML = 'Tu Suerte Está al: ' + numero + '% :(';
} else if (numero > 33 && numero < 66) {
    resultadoElemento.innerHTML = 'Tu Suerte Está al: ' + numero + '% :)';
} else if (numero > 66) {
    resultadoElemento.innerHTML = 'Tu Suerte Está al: ' + numero + '% :D';
}
}