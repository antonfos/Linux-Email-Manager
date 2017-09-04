var alias;
$(document).ready(function () {
    alias = {
        _init: false,
        domains: [],
        domainemails: [],
        current_domain: {},
        email_list: [],
        init: function () {
            if (this._init) return;
            this.bind(function () {
                log.d("aliases.js loaded");
                
            });
            this._init = true;
        },
        bind: function (cb) {
            cb = cb || null;
            getDomains("0", function (r) {
                alias.domains = r;
                if (typeof cb === "function")
                    cb();
            });
        },

        settings: {
            Getalias: "/getalias/id/",   // {id}
            getEmailsByDomain: "/emailsbydomain/", // <int:domain_id>
            Deletealias: "",
            formalias: "#form_alias"
        }
    };

    alias.DomainChange = function (domain_id) {
        getDomainName(domain_id, function (domain_name) {
            log.d("Domain Name : ", domain_name);
            if (domain_name) {
                alias.current_domain = { "domain_id": domain_id, "name": domain_name };
                getEmailsByDomain(domain_id, function (emails) {
                    if (emails) {
                        alias.email_list = emails;
                        log.d("Number of emails : ", alias.email_list.length);
                        setupForm();
                    } else {
                        alias.email_list = [];
                        showError("No email addresses defined for this domain !");
                        ShowForm(false);
                        return false;
                    }
                });
            }
        });
    };

    alias.newAlias = function(){
        ShowForm(true);
        PopulateDomainDropdown();
        reset_form();
    };


    alias.init();

    function showError(message){
        log.d("Show Error");
        //$('.errmess').delay(5000).fadeTo(500, 0).slideUp(400);

        $('errordiv').removeClass('hide');
        $('#showerror').html(message).delay(5000).fadeTo(500, 0).slideUp(400);;
    }

    function getDomains(id, cb) {
        cb = cb || null;
        log.d("Get Domain ", id);
        var url = "/domain/id/" + id
        $.ajax({
            url: url,
            dataType: "json",
            // data: $('form').serialize(),
            type: 'GET',
            success: function (r) {
                if (r.data !== null && r.status) {
                    log.d("Domains : ", r.data);
                    // emails.domains = r.data;
                    if (typeof cb === "function")
                        cb(r.data);
                }
            },
            error: function (error) {
                console.log(error);
                if (typeof cb === "function")
                    cb([]);
            }
        });
    };

    function getEmailsByDomain(id, cb) {
        cb = cb || null;
        log.d("Get Emails By Domain for ", id);
        var url = alias.settings.getEmailsByDomain + id
        $.ajax({
            url: url,
            dataType: "json",
            // data: $('form').serialize(),
            type: 'GET',
            success: function (r) {
                if (r.data !== null && r.status) {
                    log.d("emails : ", r.data);
                    // emails.domains = r.data;
                    if (typeof cb === "function")
                        cb(r.data);
                }
            },
            error: function (error) {
                console.log(error);
                if (typeof cb === "function")
                    cb([]);
            }
        });
    };

    function getDomainName(id, cb) {
        cb = cb || null;
        var dom = null;
        $.each(alias.domains, function (k, v) {
            if (parseInt(v[0]) == parseInt(id)) {
                dom = v[1];
            }
            if (k >= alias.domains.length) {
                if (typeof cb === "function")
                    cb(dom);
                return true;
            }
        });
        if (typeof cb === "function")
            cb(dom);
    }

    function ShowForm(s) {
        (s) ? $(alias.settings.formalias).removeClass('hide') : $(alias.settings.formalias).addClass('hide');
    }

    function setupForm(){
        reset_form();
        log.d("domain : ", alias.current_domain.name);
        $('#domain_id').val(alias.current_domain.domain_id);
        $('#emaildomain').html(alias.current_domain.name);
        var sel = $('#seldestination').empty();
        $.each(alias.email_list, function(k,v){
            log.d("Adding Email Address ", v);
            sel.append('<option value="' + v[2] + '"> ' + v[2] + '</option>');
        });
    }

    function reset_form(){
        $('#id').val('0');
        $('#domain_id').val(0);
        $('#email').val("");
        $('#seldestination').val("");
        $('#emaildomain').val("-------")

    }

    function PopulateDomainDropdown(){
        var sel = $('#seldomain').empty()
        sel.append('<option value="0">Select domain ....</option>');
        $.each(alias.domains, function(k,v){
            sel.append('<option value="' + v[0] + '"> ' + v[1] + '</option>');
        });
    }

    
});