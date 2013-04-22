$(function() {
    var container = $('.countdown');
    var refresh_interval = container.data('from');
    var paused = false;

    if (refresh_interval === 0) {
        container.hide();
        return;
    }

    var countdown = function(from) {
        var current = from;
        var interval_id = setInterval(function() {
            if (paused) {
                return;
            }

            current -= 1;

            container.html(current);

            if (current === 0) {
                window.clearInterval(interval_id);
                container.trigger('countdown-finished');
            }
        }, 1000);
    };

    var execute_refresh = function() {
        $('#monitors').fadeOut('slow', function() {
            $('#monitors').load(window.location.href + ' #monitors > div',
                function(response, status, xhr) {
                    if (status=="error") {
                        $('#monitors').html(
                            '<div class="small-12 columns error">Error Refreshing Monitors</div>'
                        );
                    }
                    $('#monitors').fadeIn('slow');
                });
        });
    };

    // resets countdown
    container.bind('countdown-finished', function() {
        countdown(refresh_interval);
    });

    // executes refresh
    container.bind('countdown-finished', execute_refresh);

    // pauses the refresh
    container.bind('click', function() {
        paused = ! paused;
    });

    countdown(refresh_interval);
});