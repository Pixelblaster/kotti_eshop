$(document).ready(function(){
    $('select.selectize').selectize({
        plugins: ['remove_button'],
        create:true,
        createOnBlur: true,
        diacritics: true,
        highlight:true,
        persist: false
    });
});
