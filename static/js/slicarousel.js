(function ($) {

    $.fn.slicarousel = function (options) {

        let default_options = {
            "nbr_slides": 5, // The number of slides
            "class_name_prefix": "s_", // Avoid CSS classes mixed up
            "arrows": true, // Enable the arrows navigation
            "dot_nav": true, // Enable the dots navigation
            "full_width": true, // width: 100%
            "autoplay": {
                "enabled": true, // Enable autoplay slider
                "direction": "ltr" // direction right to left rtl or left to right ltr
            },
            "delay": 9500, // The sliding delay in milliseconds
            "speed": 200 // The sliding speed can be slow, normal, fast or customized in milliseconds
        }

        // Handling the speed option
        switch (default_options.speed) {
            case "fast":
                default_options.speed = 250
                break;

            case "normal":
                default_options.speed = 500
                break;

            case "slow":
                default_options.speed = 1000
                break;
        }

        let params = $.extend(default_options, options);
        this.append("<div class='" + params.class_name_prefix + "slider_container'></div>")
        $(this.children()[0]).css({
            "width": ((params.nbr_slides + 1) * 100) + "%"
        })

        let i = 0
        while (i < params.nbr_slides) {
            $(this.children()[0]).append("<div class='" + params.class_name_prefix + "slide " + params.class_name_prefix + "slide_" + i + "'><div class='landing-overlay'></div></div>")
            i++
        }

        $(this.children()[0]).append("<div class='" + params.class_name_prefix + "slide " + params.class_name_prefix + "slide_0'><div class='landing-overlay'></div></div>")
        $("." + params.class_name_prefix + "slide").css({
            "width": (100 / (params.nbr_slides + 1)) + "%"
        })

        let current_slide = 0 // the slide number where the mouse is in
        let mousedown_position = 0 // the silde number where the mouse starts grabbing
        let mouseup_position = 0 // the slide number where the mouse finished grabbing
        let direction = true // false: from the left to the right // true: means from the right to the left
        let parent_offset_left = 0

        $(this.children()[0]).mousedown((e) => {
            is_down = true
            parent_offset_left = $(this).offset().left
            mousedown_position = e.pageX - parent_offset_left
        }).mouseup((e) => {
            is_down = false
            parent_offset_left = $(this).offset().left
            mouseup_position = e.pageX - parent_offset_left

            if ((mouseup_position - mousedown_position) > 0) {
                // test if the user really wants to swip
                if ((mouseup_position - mousedown_position) > 30)
                    direction = true
                else
                    direction = null
            } else {
                // test if the user really wants to swip
                if ((mouseup_position - mousedown_position) < -30)
                    direction = false
                else
                    direction = null
            }
            if (direction != null) {
                if (!direction) {
                    if (current_slide < params.nbr_slides) {
                        current_slide++
                        if (current_slide == params.nbr_slides) {
                            $(this.children()[0]).animate({
                                "left": -(current_slide * 100) + "%"
                            }, params.speed, function () {
                                $(this).css({
                                    "left": "0%"
                                })
                            })
                            current_slide = 0
                        } else {
                            $(this.children()[0]).animate({
                                "left": -(current_slide * 100) + "%"
                            }, params.speed)
                        }
                    }
                } else {
                    if (current_slide >= 0) {
                        current_slide--
                        if (current_slide == -1) {
                            $(this.children()[0]).css({
                                "left": "-" + (params.nbr_slides * 100) + "%"
                            })
                            current_slide = params.nbr_slides - 1

                            $(this.children()[0]).animate({
                                "left": -(current_slide * 100) + "%"
                            }, params.speed)

                        } else {
                            $(this.children()[0]).animate({
                                "left": -(current_slide * 100) + "%"
                            }, params.speed)
                        }
                    }
                }
            }
            // If the dots navigation is enabled
            if (params.dot_nav) {
                $(".dot").each(function () {
                    if ($(this).hasClass('active'))
                        $(this).removeClass('active')
                })
                $(".dot-" + current_slide).addClass("active")
            }
        })

        // the slider
        let _this = $(".the_slider")

        // go to the next slide
        let next_slide = (_this) => {
            if (current_slide < params.nbr_slides) {
                current_slide++
                if (current_slide == params.nbr_slides) {
                    $(_this.children()[0]).animate({
                        "left": -(current_slide * 100) + "%"
                    }, params.speed, function () {
                        $(this).css({
                            "left": "0%"
                        })
                    })

                    current_slide = 0
                } else {
                    $(_this.children()[0]).animate({
                        "left": -(current_slide * 100) + "%"
                    }, params.speed)
                }

                // If the dots navigation is enabled
                if (params.dot_nav) {
                    $(".dot").each(function () {
                        if ($(this).hasClass('active'))
                            $(this).removeClass('active')
                    })

                    $(".dot-" + current_slide).addClass("active")
                }
            }
        }

        // go to the prevouis slide
        let prev_slide = (_this) => {
            if (current_slide >= 0) {
                current_slide--
                if (current_slide == -1) {
                    $(_this.children()[0]).css({
                        "left": "-" + (params.nbr_slides * 100) + "%"
                    })
                    current_slide = params.nbr_slides - 1
                    $(_this.children()[0]).animate({
                        "left": -(current_slide * 100) + "%"
                    }, params.speed)

                } else {
                    $(_this.children()[0]).animate({
                        "left": -(current_slide * 100) + "%"
                    }, params.speed)
                }
                // If the dots navigation is enabled
                if (params.dot_nav) {
                    $(".dot").each(function () {
                        if ($(this).hasClass('active'))
                            $(this).removeClass('active')
                    })
                    $(".dot-" + current_slide).addClass("active")
                }
            }
        }

        // Adding the arrows functionality.
        if (params.arrows) {
            let next = "<a class='carousel-control-next' href='#mycarousel' role='button' data-slide='next'><div class='banner-icons'><span class='fas fa-angle-right home-right'></span></div><span class='sr-only'>Next</span></a>"
            let prev = "<a class='carousel-control-next' href='#mycarousel' role='button' data-slide='next'><div class='banner-icons'><span class='fas fa-angle-left home-left'></span></div><span class='sr-only'>Next</span></a>"
            this.append("<div class='" + params.class_name_prefix + "arrows arrows'><span class='prev'>" + prev + "</span><span class='next'>" + next + "</span></div>")

            $(".arrows .next").on("click", () => {
                next_slide(_this)
            })

            $(".arrows .prev").on("click", () => {
                prev_slide(_this)
            })

        }

        // Adding the dots navigation
        if (params.dot_nav) {
            this.append("<div class='dot_nav'></div>")
            for (let i = 0; i < params.nbr_slides; i++) {
                if (i == 0)
                    $(".dot_nav").append("<span class='dot dot-" + i + " active' slide-nbr='" + i + "'></span>")
                else
                    $(".dot_nav").append("<span class='dot dot-" + i + "' slide-nbr='" + i + "'></span>")
            }
            $(".dot").each(function () {
                $(this).on("click", function () {
                    if (!$(this).hasClass()) {
                        $(".dot").each(function () {
                            if ($(this).hasClass('active'))
                                $(this).removeClass('active')
                        })
                        $(this).addClass("active")
                        if (current_slide != $(this).attr('slide-nbr')) {
                            ($(".s_slider_container")).animate({
                                "left": -($(this).attr('slide-nbr') * 100) + "%"
                            }, Math.abs(current_slide - $(this).attr('slide-nbr')) * params.speed)
                            current_slide = $(this).attr('slide-nbr')
                        }
                    }
                })
            })
        }

        // Adding the autoplay functionality.
        if (params.autoplay.enabled) {

            if (params.autoplay.direction === "ltr" || params.autoplay.direction === "rtl") {
                let interval = setInterval(() => {
                    if (params.autoplay.direction === "ltr")
                        prev_slide(_this)
                    else
                        next_slide(_this)

                }, params.delay)

                _this.on("mouseenter", () => {
                    clearInterval(interval)
                })

                _this.on("mouseleave", () => {
                    interval = setInterval(() => {
                        if (params.autoplay.direction === "ltr")
                            prev_slide(_this)
                        else
                            next_slide(_this)

                    }, params.delay)
                })
            } else {
                console.error("Error: options.autoplay.direction should be \"ltr\" or \"rtl\".")
            }


        }

        // handling the full width option
        if (!params.full_width) {
            $(this).css({
                "width": "100%"
            })
            $(".s_slide").css({
                "width": "12%",
                "margin": "0 2.333%"
            })
        }
    }
    return this;
})(jQuery);
