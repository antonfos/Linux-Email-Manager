var alias;
$(document).ready(function () {
    alias = {
        _init: false,
        domains: [],
        domainemails: [],
        current_domain: {},
        email_list: [],
        current_alias: {},
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
            FetchAlias: "/fetchalias/", // <int:alias_id>
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
        $('#source').prop('readonly', false);
        $('#seldomain').prop('disabled', false);
        $('#emaildomain').html("-------")
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

    alias.submit = function(){
        log.d("Form Submit");
    }

    alias.delAlias = function(){
        log.d("Current Alias ",alias.current_alias, $('#id').val() ) ;
        bootbox.confirm("Confirm delete alias (" +alias.current_alias[0]+ ") "+alias.current_alias[2]+" !", function(r){
            if (r){
                log.d("Deteling Alias ", alias.current_alias[2]);
                $('#_method').val("DELETE");
                
                $('#alias_form').submit();
            }
        });
    };

    alias.clear = function(){
         ShowForm(false);
     };

    alias.getAlias = function(id){
        log.d("Get the alias for id ", id);
        GetAlias(id, function(falias){
            log.d("[getAlias] Alias ", falias);
            if (falias){
                alias.current_alias = falias[0];
                var src_split = alias.current_alias[2].split("@");
                log.d("Email Split ", src_split);
                // Populate the form
                getEmailsByDomain(alias.current_alias[1], function(emails){
                    if (emails) {
                        alias.email_list = emails;
                        ShowForm(true);
                        PopulateDomainDropdown();
                        setupForm();
                        $('#seldomain').val(alias.current_alias[1]).prop('disabled', true);
                        $('#id').val(alias.current_alias[0]);
                        $('#source').val(src_split[0]).prop('readonly', true);
                        $('#seldestination').val(alias.current_alias[3]);
                        $('#emaildomain').html(src_split[1]);
                    }
                });
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
        log.d("loading the emails ", alias.email_list);
        $.each(alias.email_list, function(k,v){
            log.d("Adding Email Address ", v);
            sel.append('<option value="' + v[2] + '"> ' + v[2] + '</option>');
        });
        $('#source').prop('readonly', false);
        sel.prop('disabled', false);
    }

    function reset_form(){
        $('#id').val('0');
        $('#domain_id').val("0");
        $('#source').val("");
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

    function GetAlias(alias_id, cb){
        cd = cb || null;
        var url = alias.settings.FetchAlias  + alias_id
        log.d("Fetch Alias URL ", url);
        $.ajax({
            url: url,
            dataType: "json",
            // data: $('form').serialize(),
            type: 'GET',
            success: function (r) {
                if (r.data !== null && r.status) {
                    log.d("alias : ", r.data);
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
    }

    
});