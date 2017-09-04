/* Main App js */
var siteDebug = true;

var log = {
    _log: function (type, args) {
        if (!siteDebug) {
            return false;
        }
        var args = Array.prototype.slice.call(args);
        var time = new Date().toISOString();
        args.unshift(time);
        console[type].apply(console, args);
        return true;
    },
    d: function () {
        log._log('log', arguments);
    },
    i: function () {
        log._log('info', arguments);
    },
    e: function () {
        log._log('error', arguments);
    },
    w: function () {
        log._log('warn', arguments);
    }
};

version = function(){ log.d('app.js loaded'); }

version();


$('.flashalert').not('alert-danger').delay(5000).fadeTo(500, 0).slideUp(400);


