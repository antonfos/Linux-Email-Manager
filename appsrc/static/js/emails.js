var emails;
$(document).ready(function () {
    emails = {
        _init: false,
        addresses: [],
        domains: [],
        seldomain : 0,
        seldomainname: "",
        curemail: {},
        init: function () {
            if (this._init) return;
            this.bind(function () {
                log.d("emails.js loaded");
            });
            this.setDomain("0");
            this._init = true;
        },
        bind: function (cb) {
            cb = cb || null;
            getDomains("0", function(r){
                emails.domains = r;
                if (typeof cb === "function")
                    cb();
            });
        },
        settings: {
            Getemail: "/emails/%d",   // {id}
            GetEmailsByDomain: "/email/%d/domain",
            DeleteDomain: "",
            formemail: "#form_email"
        }
    };

    emails.delEmail = function(){
        log.d("Current Email ",emails.curemail, $('#id').val() ) ;
        bootbox.confirm("Confirm delete email (" +emails.curemail[0]+ ") "+emails.curemail[2]+" !", function(r){
            if (r){
                log.d("Deteling Email ", emails.curemail[2]);
                $('#_method').val("DELETE");
                
                $('#email_form').submit();
            }
        });
        // ResetForm();
        // emails.curemail = {};
        // ShowForm(false);
    };

    emails.setDomain = function (value) {
        emails.seldomain = parseInt(value);
        getDomainName(emails.seldomain, function(domain){
            log.d("Found Domain : ", domain);
            if (domain){
                emails.seldomainname = domain;
                emails.seldomain = emails.seldomain;
            }
        });
        log.d("Domain ", emails.seldomainname);
        ResetForm();
        clearEmailList();
        log.d("Domain Selected ", value);
        var url = "/email/" + value + "/domain"
        log.d("Domain Selected url ", url);
        $.ajax({
            url: url,
            dataType: "json",
            // data: $('form').serialize(),ee
            type: 'GET',
            success: function (response) {
                //response = JSON.parse(response);
                if (response.data !== null && response.status) {
                    log.d("Response : ", response.data);
                    emails.addresses = response.data;
                    PopulateEmailList();
                    // ShowForm(true)
                    // $('#id').val(response.data[0][0]);
                    // $('#domain').val(response.data[0][1]);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    };

    emails.getEmail = function (id) {
        ResetForm();
        $('#_method').val("POST");
        log.d("Email Selected ", id);
        var url = "/emails/" + id 
        log.d("Get Email id Selected url ", url);
        $.ajax({
            url: url,
            dataType: "json",
            // data: $('form').serialize(),
            type: 'GET',
            success: function (response) {
                //response = JSON.parse(response);
                if (response.data !== null && response.status) {
                    log.d("Response : ", response.data[0]);
                    emails.curemail = response.data[0];
                    var email_split = emails.curemail[2].split("@");
                    log.d("Email Split ", email_split);
                    ShowForm(true);
                    $('#id').val(emails.curemail[0]);
                    $('#domain_id').val( emails.curemail[1] );
                    $('#email').val( email_split[0] );
                    $('#email').prop("readonly", true);
                    $('#name').val(emails.curemail[3]);
                    $('#emaildomain').empty().html( email_split[1] )
                    $('#passwd').val("");
                    getDomainName(emails.curemail[1], function(domain){
                        log.d("Found Domain : ", domain);
                        if (domain){
                            emails.seldomainname = domain;
                            emails.seldomain = emails.curemail[1];
                        }
                    })

                    // ShowForm(true)
                    // $('#id').val(response.data[0][0]);
                    // $('#domain').val(response.data[0][1]);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    };

    emails.newemail = function(){
        $('#_method').val("POST");
        log.d("newemail ", emails.seldomain );
        if (checkIsAddAvailable() === false) return false;
        ResetForm();
        getDomainName(emails.seldomain, function(domain){
            log.d("Found Domain : ", domain);
            if (domain){
                emails.seldomainname = domain;
                ShowForm(true);
                $('#emaildomain').empty().html( domain )
                $('#id').val("0");
                $('#domain_id').val( emails.seldomain );
                $('#email').focus();
                $('#email').prop("readonly", false);
            }
        });
        
    };

    emails.submit = function(){
        log.d("Submit Form");
    }

    emails.clear = function(){
         ShowForm(false);
     };

    emails.init();

    function ResetForm(){
        $('#id').val("0");
        $('#email').val("");
        $('#name').val("");
        $('#passwd').val("");
    }

    function PopulateEmailList(){
        tbl = $('#emaillist').empty();
        //tbl.append("<option value='0'>All</option>");
        $.each(emails.addresses, function(k,v){
            tbl.append('<tr><td><a href="javascript:void(0)" class="alink" onclick="emails.getEmail(this.id);" id="'+v[0]+'">'+v[3]+'</a></td></tr>');
        });
    }

    function clearEmailList(){
        $('#emaillist').empty();
    }

    function getDomains(id, cb){
        cb = cb || null;
        log.d("Get Domain ", id);
        var url = "/domain/id/"+id
        $.ajax({
            url: url,
            dataType: "json",
            // data: $('form').serialize(),
            type: 'GET',
            success: function(r) {
                if (r.data !== null && r.status) {
                log.d("Domains : ", r.data);
                // emails.domains = r.data;
                if (typeof cb === "function")
                    cb(r.data);
                }
            },
            error: function(error) {
                console.log(error);
                if (typeof cb === "function")
                    cb([]);
            }
        });
    };

    function checkIsAddAvailable(){
        if ( parseInt(emails.seldomain) === 0 || email.seldomainname === "" ){
            alert("You must select a domain above before you can add an email account!");
            return false;
        }
        return true;
    }

    function getDomainName(id, cb){
        cb = cb || null;
        var dom = null;
        $.each(emails.domains, function(k,v){
            if (parseInt(v[0]) == parseInt(id)){
                dom = v[1];
            }
            if (k >= emails.domains.length ){
                if (typeof cb === "function")
                    cb( dom );
                return true;
            } 
        });
        if (typeof cb === "function")
              cb( dom );
    }

    function ShowForm(s){
        (s) ? $(emails.settings.formemail).removeClass('hide') : $(emails.settings.formemail).addClass('hide');
    }

});

