function student() {
    window.location.href = '/students';
  }

function adstudent() {
    window.location.href = '/adstudent';
}

function delstudent() {
    window.location.href = '/delstudent';
}

function upstudent() {
    window.location.href = '/upstudent';
}

function teachers() {
    window.location.href = '/teachers';
}

function adteacher() {
    window.location.href = '/adteacher';
}

function delteacher() {
    window.location.href = '/delteacher';
}

function upteacher() {
    window.location.href = '/upteacher';
}

function subjects() {
    window.location.href = '/subjects';
}

function adsubject() {
    window.location.href = '/adsubject';
}

function delsubject() {
    window.location.href = '/delsubject';
}

function upsubject() {
    window.location.href = '/upsubject';
}

function addstudent() {
    window.location.href = '/addstudent';
}

function users() {
    window.location.href = '/users';
}

function aduser() {
    window.location.href = '/aduser';
}

function deluser() {
    window.location.href = '/deluser';
}

$(document).ready(function () {
    $('#dtBasicExample').DataTable();
    $('.dataTables_length').addClass('bs-select');
  });