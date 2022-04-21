$('#phone').mask("(99) 99999-9999", {removeMaskOnSubmit: true});
$('#zip_code').mask("99999-999", {removeMaskOnSubmit: true});
$('#cpf').mask("999.999.999-99", {removeMaskOnSubmit: true});
$("#zip_code").focusout(function () {
    //Início do Comando AJAX
    $.ajax({
        //O campo URL diz o caminho de onde virá os dados
        //É importante concatenar o valor digitado no CEP
        url: 'https://viacep.com.br/ws/' + $(this).val() + '/json/unicode/',
        //Aqui você deve preencher o tipo de dados que será lido,
        //no caso, estamos lendo JSON.
        dataType: 'json',
        //SUCESS é referente a função que será executada caso
        //ele consiga ler a fonte de dados com sucesso.
        //O parâmetro dentro da função se refere ao nome da variável
        //que você vai dar para ler esse objeto.
        success: function (resposta) {
            //Agora basta definir os valores que você deseja preencher
            //automaticamente nos campos acima.
            $("#address").val(resposta.logradouro);
            $("#city").val(resposta.localidade);
            //Vamos incluir para que o Número seja focado automaticamente
            //melhorando a experiência do usuário
            $("#number").focus();
        }
    });
});

$("#cpf").focusout(function () {
    var numeros, digitos, soma, i, resultado, digitos_iguais;
    var cpf = $("#cpf").val().replace(/[^0-9]/g, '');
    $("#cpf_wrong").text('');
    digitos_iguais = 1;
    if (cpf.length < 11)
        return $("#cpf").text('');
    for (i = 0; i < cpf.length - 1; i++)
        if (cpf.charAt(i) != cpf.charAt(i + 1)) {
            digitos_iguais = 0;
            break;
        }
    if (!digitos_iguais) {
        numeros = cpf.substring(0, 9);
        digitos = cpf.substring(9);
        soma = 0;
        for (i = 10; i > 1; i--)
            soma += numeros.charAt(10 - i) * i;
        resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
        if (resultado != digitos.charAt(0)) {
            $("#cpf").val('');
        }
        numeros = cpf.substring(0, 10);
        soma = 0;
        for (i = 11; i > 1; i--)
            soma += numeros.charAt(11 - i) * i;
        resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
        if (resultado != digitos.charAt(1)) {
            $("#cpf").val('');
        }
    } else {
        $("#cpf").val('');
    }
});