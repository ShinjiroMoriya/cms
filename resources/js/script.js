$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
         }
     },
     timeout : 30000
});

$('form').on('submit', function() {
    $(document).find('#loading').show();
});

$('body').append('<div id="loading" class="loading"></div>');


$('.status_select').on('change', function() {
    var lang = $(this).attr('data-lang');
    var post_type = $(this).attr('data-post_type');
    var post_id = $(this).attr('data-post_id');
    var status = $(this).val();
    if (post_type === 'introduction') {
        var endpoint = '/' + lang + '/api/introductions/' + post_id + '/status';
    }
    if (post_type === 'video') {
        var endpoint = '/' + lang + '/api/videos/' + post_id + '/status';
    }
    if (post_type === 'topic') {
        var endpoint = '/' + lang + '/api/topics/' + post_id + '/status';
    }

    $.ajax({
        type: 'POST',
        url: endpoint,
        cache: false,
        data: {
            'status': status
        },
        context: this

    }).done(function(data) {
        $('.header_status_text').text('更新しました');
        $('.header_status').addClass('_show _success');

    }).fail(function(jqXHR) {
        var data = jqXHR.responseJSON;
        if (jqXHR.status === 503) {
            $('.header_status_text').text(data.message);
            $('.header_status').addClass('_show _error');
        } else {
            $('.header_status_text').text('通信エラー');
            $('.header_status').addClass('_show _error');
        }
        $(this).val($(this).data('choice'));

    }).always(function(data) {
        setTimeout(function() {
            $('.header_status_text').text('');
            $('.header_status').removeClass('_show _success _error');
        }, 2000);
    });
});


$('.new_checked').on('change', function() {
    var lang = $(this).attr('data-lang');
    var post_type = $(this).attr('data-post_type');
    var post_id = $(this).attr('data-post_id');
    var new_flag = $(this).prop('checked');
    if (post_type === 'topic') {
        var endpoint = '/' + lang + '/api/topics/' + post_id + '/new';
    }

    $.ajax({
        type: 'POST',
        url: endpoint,
        cache: false,
        data: {
            'new': new_flag
        },
        context: this

    }).done(function(data) {
        $('.header_status_text').text('更新しました');
        $('.header_status').addClass('_show _success');

    }).fail(function(jqXHR) {
        var data = jqXHR.responseJSON;
        if (jqXHR.status === 503) {
            $('.header_status_text').text(data.message);
            $('.header_status').addClass('_show _error');
        } else {
            $('.header_status_text').text('通信エラー');
            $('.header_status').addClass('_show _error');
        }
        $(this).val($(this).data('choice'));

    }).always(function(data) {
        setTimeout(function() {
            $('.header_status_text').text('');
            $('.header_status').removeClass('_show _success _error');
        }, 2000);
    });
});

$('#delete_button').on('click', function() {
    if (!window.confirm('削除してよろしいですか？')) {
        return false;
    }
});

if ($('.input_image_add_button').length != 0) {
  $('.input_image_add_button').on('click', function() {
      var image_type = $(this).attr('data-image_type');
      $('#upload').attr('data-image_type', image_type);
      $('#upload').click();
  });
  $('#upload').on('change', function(event) {

      var lang = $(this).attr('data-lang');
      var refresh_href = $(this).attr('data-refresh_href');
      var image_type = $(this).attr('data-image_type');

      $('#image_upload').off('submit');
      $('#image_upload').on('submit', function(e) {

          e.stopPropagation();
          e.preventDefault();

          var fd = new FormData();
          $.each(event.target.files, function(i, file) {
              fd.append('image_file', file);
          });
          $('#loading').show();
          $.ajax({
              type: 'POST',
              url: '/' + lang + '/api/images/add',
              cache: false,
              data: fd,
              processData: false,
              contentType: false
          }).done(function(data) {

              if (refresh_href) {
                  window.location.href = refresh_href;
              }

              var image_pk = data.id
              var image_url = data.image_url
              var thumbnail = image_url.replace( '/image/upload/', '/image/upload/w_250,h_250,c_pad,b_white/');

              if (image_type === 'thumbnail') {
                  $('#image_thumbnails_2').html('<div><input type="hidden" name="thumbnail" value="' + image_url + '"><img src="' + thumbnail + '" alt=""><span class="thumbnail_delete">取消</span></div>');
              } else if (image_type === 'image') {
                  $('#image_thumbnails_2').html('<div><input type="hidden" name="image" value="' + image_url + '"><img src="' + thumbnail + '" alt=""><span class="thumbnail_delete">取消</span></div>');
              } else {
                  $('#image_thumbnails_1').append('<div><input type="hidden" name="images" value="' + image_pk + '"><img src="' + thumbnail + '" alt=""><span class="thumbnail_delete">取消</span></div>')
              }

              if ($('#empty_image').length === 1) {
                  $('#empty_image').remove();
              }

          }).fail(function(jqXHR) {
              $('.header_status_text').text('通信エラー');
              $('.header_status').addClass('_show _error');

          }).always(function() {
              $('input[name="image_file"]').val('');
              $('#loading').hide();
              setTimeout(function() {
                  $('.header_status_text').text('');
                  $('.header_status').removeClass('_show _success _error');
              }, 2000);
          });
      });

      $('#image_upload').trigger('submit');

  });
}

function limit_text(txt) {

    if (!txt) return txt;

    if(txt.length > 25) {
        txt = txt.substr(0, 25) + '...';
    }
    return txt
}

$('.input_image_list_add_button').on('click', function() {
    var image_block = $(this).parents("tr");
    if (image_block.find('.image_list').find('li').length !== 0) { return false; }
    if ($('#empty_image').length === 1) { return false; }
    var lang = $(this).attr('data-lang');
    image_block.find('.image_list_block').show();
    $.ajax({
        type: 'GET',
        url: '/' + lang + '/api/images',
        cache: false

    }).done(function(data) {
        $.each(data.images, function(i, image) {
            image_block.find('.image_list').append('<li><a href="' + image.image_url + '" data-lity class="a_link">' + limit_text(image.title) + '</a> <a href="javascript:;" class="a_link choice_image" data-image_url="' + image.image_url + '" data-image_pk="' + image.id + '">選択</a>・<a href="' + image.image_url + '" data-lity class="a_link">確認</a></li>');
        });

        if (data.total !== 1 && data.total != data.paged && data.total !== 0) {
            image_block.find('.image_list').parent().append('<a href="javascript:;" class="a_link image_more_link"' + 'data-paged="' + (data.paged + 1) + '"' + 'data-lang="' + lang + '">さらに読み込む</a>')
        }

        if (data.total === 0) {
            image_block.find('.image_list').parent().append(
            '<p id="empty_image">画像は登録されていません。</p>')
        } else {
            $('#empty_image').remove();
        }

        if (data.total === data.paged) {
            image_block.find('.image_list').parent().find('.more_link').remove();
        }

    }).fail(function(jqXHR) {
        $('.header_status_text').text('通信エラー');
        $('.header_status').addClass('_show _error');

    }).always(function() {
        setTimeout(function() {
            $('.header_status_text').text('');
            $('.header_status').removeClass('_show _error');
        }, 2000);
    });
});

$(document).on('click', '.image_more_link', function() {

    var lang = $(this).attr('data-lang');
    var paged = $(this).attr('data-paged');
    var image_block = $(this).parents("tr");

    $.ajax({
        type: 'GET',
        url: '/' + lang + '/api/images/' + paged,
        cache: false

    }).done(function(data) {
        $.each(data.images, function(i, image) {
            image_block.find('.image_list').append('<li><a href="' + image.image_url + '" data-lity class="a_link">' + limit_text(image.title) + '</a> <a href="javascript:;" class="a_link choice_image" data-image_url="' + image.image_url + '" data-image_pk="' + image.id + '">選択</a>・<a href="' + image.image_url + '" data-lity class="a_link">確認</a></li>');
        });

        if (data.total !== 1 && data.total != data.paged && data.total !== 0) {
            image_block.find('.image_list').append('<li><a href="javascript:;" class="a_link image_more_link"' + 'data-paged="' + (data.paged + 1) + '"' + 'data-lang="' + lang + '">さらに読み込む</a></li>')
        }

        if (data.total === data.paged) {
            image_block.find('.image_list').find('.image_more_link').remove();
        }

    }).fail(function(jqXHR) {
        $('.header_status_text').text('通信エラー');
        $('.header_status').addClass('_show _error');

    }).always(function() {
        setTimeout(function() {
            $('.header_status_text').text('');
            $('.header_status').removeClass('_show _error');
        }, 2000);
    });

});

$(document).on('click', '.choice_image', function() {
    var image_type = $(this).parents('.image_list').attr('data-image_type');
    var image_pk = $(this).attr('data-image_pk');
    var image_url = $(this).attr('data-image_url');
    var thumbnail = image_url.replace('/image/upload/', '/image/upload/w_250,h_250,c_pad,b_white/');

    if (image_type === 'thumbnail') {
        $('#image_thumbnails_2').html('<div><input type="hidden" name="thumbnail" value="' + image_url + '"><img src="' + thumbnail + '" alt=""><span class="thumbnail_delete">取消</span></div>');
    } else if (image_type === 'image') {
        $('#image_thumbnails_2').html('<div><input type="hidden" name="image" value="' + image_url + '"><img src="' + thumbnail + '" alt=""><span class="thumbnail_delete">取消</span></div>');
    } else {
        $('#image_thumbnails_1').append('<div><input type="hidden" name="images" value="' + image_pk + '"><img src="' + thumbnail + '" alt=""><span class="thumbnail_delete">取消</span></div>')
    }
});

$(document).on('click', '.thumbnail_delete', function() {
    $(this).parent().remove();
});

$('.image_delete_check').on('click', function(e) {

    var lang = $(this).attr('data-lang');
    var image_id = $(this).attr('data-image_id');
    var image_delete_href = $(this).attr('data-href');

    $.ajax({
        type: 'GET',
        url: '/' + lang + '/api/images/delete/' + image_id,
        cache: false

    }).done(function(data) {
        if (data.delete_flag === true) {
            if (!window.confirm('削除してよろしいですか？')) {
                return false;
            }
            window.location.href = image_delete_href;

        } else {
            $('#use_images_list').html('');
            $.each(data.use_posts, function(i, use_post) {
                $('#use_images_list').append('<li><a target="_blank" href="/' + use_post.lang + '/admin/' + use_post.post_type + '/' + use_post.id + '" class="a_link">' +  limit_text(use_post.title) + '（' + use_post.post_type_label + '）</a></li>');
            });
            $('#use_images_link').click();
        }

    }).fail(function(jqXHR) {
        $('.header_status_text').text('通信エラー');
        $('.header_status').addClass('_show _error');

    }).always(function() {
        setTimeout(function() {
            $('.header_status_text').text('');
            $('.header_status').removeClass('_show _error');
        }, 2000);
    });
});

function get_titles(paged, lang, value) {
    $.ajax({
        type: 'GET',
        url: '/' + lang + '/api/titles/' + paged,
        cache: false,
        data: {'value': value}

    }).done(function(data) {

        $.each(data.titles, function(i, title) {
            var _title = title.title;
            $('#titles_list').append('<li>' + limit_text(_title) + ' <a href="javascript:;" class="a_link choice_list" data-add_id="' + title.id + '" data-post_title="' + limit_text(_title) + '" data-post_type="titles">選択</a></li>');
        });

        if (data.total !== 1 && data.total != data.paged && data.total !== 0) {
            $('#titles_list').append('<li><a href="javascript:;" class="a_link title_more_link" data-paged="' + (data.paged + 1) + '">さらに読み込む</a></li>')
        }

        if (data.total === data.paged) {
            $('#titles_list').find('.title_more_link').remove();
        }

    }).fail(function(jqXHR) {
        $('.header_status_text').text('通信エラー');
        $('.header_status').addClass('_show _error');

    }).always(function() {
        setTimeout(function() {
            $('.header_status_text').text('');
            $('.header_status').removeClass('_show _error');
        }, 2000);
    });
}

if ($('#titles_list').length != 0) {
    var lang = $('#titles_list').attr('data-lang');
    get_titles(1, lang, null);
}

$(document).on('click', '.title_more_link', function() {
    var lang = $('#titles_list').attr('data-lang');
    var paged = $(this).attr('data-paged');
    $(this).remove();
    get_titles(paged, lang, null);
});

$('.titles_search_button').on('click', function() {
    $('#titles_list').find('li').remove();
    var lang = $('#titles_list').attr('data-lang');
    var value = $('.titles_search').val();
    get_titles(1, lang, value);
});

function get_videos(paged, lang, video_id, value) {
    $.ajax({
        type: 'GET',
        url: '/' + lang + '/api/videos/' + paged,
        cache: false,
        data: {
            'post_id': video_id,
            'value': value
        }

    }).done(function(data) {

        $.each(data.videos, function(i, video) {
            var _title = video.title;
            $('#videos_list').append('<li>' + limit_text(_title) + ' <a href="javascript:;" class="a_link choice_list" data-add_id="' + video.id + '" data-post_title="' + limit_text(_title) + '" data-post_type="videos">選択</a></li>');
        });

        if (data.total !== 1 && data.total !== data.paged && data.total !== 0) {
            $('#videos_list').append('<li><a href="javascript:;" class="a_link video_more_link" data-paged="' + (data.paged + 1) + '">さらに読み込む</a></li>');
        }

        if (data.total === data.paged) {
            $('#videos_list').find('.video_more_link').remove();
        }

    }).fail(function(jqXHR) {
        $('.header_status_text').text('通信エラー');
        $('.header_status').addClass('_show _error');

    }).always(function() {
        setTimeout(function() {
            $('.header_status_text').text('');
            $('.header_status').removeClass('_show _error');
        }, 2000);
    });
}

if ($('#videos_list').length != 0) {
    var lang = $('#videos_list').attr('data-lang');
    var video_id = $('#videos_list').attr('data-video_id');
    get_videos(1, lang, video_id, null);
}

$(document).on('click', '.video_more_link', function() {
    var lang = $('#videos_list').attr('data-lang');
    var video_id = $('#videos_list').attr('data-video_id');
    var paged = $(this).attr('data-paged');
    var value = $('.videos_search').val();
    $(this).remove();
    get_videos(paged, lang, video_id, value);
});

$('.videos_search_button').on('click', function() {
    $('#videos_list').find('li').remove();
    var lang = $('#videos_list').attr('data-lang');
    var video_id = $('#videos_list').attr('data-video_id');
    var value = $('.videos_search').val();
    get_videos(1, lang, video_id, value);
});

function get_introductions(paged, lang, value) {
    $.ajax({
        type: 'GET',
        url: '/' + lang + '/api/introductions/' + paged,
        cache: false,
        data: {'value': value}

    }).done(function(data) {

        $.each(data.introductions, function(i, introduction) {
            var _name = introduction.name;
            $('#introductions_list').append('<li>' + limit_text(_name) + ' <a href="javascript:;" class="a_link choice_list" data-add_id="' + introduction.id + '"' + 'data-post_title="' + limit_text(_name) + '" data-post_type="introductions">選択</a></li>');
        });

        if (data.total !== 1 && data.total !== data.paged && data.total !== 0) {
            $('#introductions_list').append('<li><a href="javascript:;" class="a_link introduction_more_link" data-paged="' + (data.paged + 1) + '">さらに読み込む</a></li>')
        }

        if (data.total === data.paged) {
            $('#introductions_list').find('.introduction_more_link').remove();
        }

    }).fail(function(jqXHR) {
        $('.header_status_text').text('通信エラー');
        $('.header_status').addClass('_show _error');

    }).always(function() {
        setTimeout(function() {
            $('.header_status_text').text('');
            $('.header_status').removeClass('_show _error');
        }, 2000);
    });
}

if ($('#introductions_list').length != 0) {
    var lang = $('#introductions_list').attr('data-lang');
    get_introductions(1, lang, null);
}

$(document).on('click', '.introduction_more_link', function() {
    var lang = $('#introductions_list').attr('data-lang');
    var paged = $(this).attr('data-paged');
    var value = $('.introductions_search').val();
    $(this).remove();
    get_introductions(paged, lang, value);
});

$('.introductions_search_button').on('click', function() {
    $('#introductions_list').find('li').remove();
    var lang = $('#introductions_list').attr('data-lang');
    var value = $('.introductions_search').val();
    get_introductions(1, lang, value);
});

function get_topics(paged, lang, value) {
    $.ajax({
        type: 'GET',
        url: '/' + lang + '/api/topics/' + paged,
        cache: false,
        data: {'value': value}

    }).done(function(data) {

        $.each(data.topics, function(i, topic) {
            var _title = topic.title;
            $('#topics_list').append('<li>' + limit_text(_title) + ' <a href="javascript:;" class="a_link choice_list" data-add_id="' + topic.id + '" data-post_title="' + limit_text(_title) + '" data-post_type="topics">選択</a></li>');
        });

        if (data.total !== 1 && data.total !== data.paged && data.total !== 0) {
            $('#topics_list').append('<li><a href="javascript:;" class="a_link topic_more_link" data-paged="' + (data.paged + 1) + '">さらに読み込む</a></li>')
        }

        if (data.total === data.paged) {
            $('#topics_list').find('.topic_more_link').remove();
        }

    }).fail(function(data) {
        $('.header_status_text').text('通信エラー');
        $('.header_status').addClass('_show _error');

    }).always(function(data) {
        setTimeout(function() {
            $('.header_status_text').text('');
            $('.header_status').removeClass('_show _error');
        }, 2000);
    });
}

if ($('#topics_list').length != 0) {
    var lang = $('#topics_list').attr('data-lang');
    get_topics(1, lang, null);
}

$(document).on('click', '.topic_more_link', function() {
    var lang = $('#topics_list').attr('data-lang');
    var paged = $(this).attr('data-paged');
    var value = $('.topics_search').val();
    $(this).remove();
    get_topics(paged, lang, value);
});

$('.topics_search_button').on('click', function() {
    $('#topics_list').find('li').remove();
    var lang = $('#topics_list').attr('data-lang');
    var value = $('.topics_search').val();
    get_topics(1, lang, value);
});

function get_categories() {
    $.ajax({
        type: 'GET',
        url: '/api/groups',
        cache: false

    }).done(function(data) {
        $.each(data.groups, function(i, group) {
            $('#categories_list').append('<li class="_group">' + group.name + '</li>');
            $.each(group.categories, function(i, category) {
                var _name = category.name_ja + ' / ' + category.name_en;
                $('#categories_list').append('<li>' + limit_text(_name) + ' <a href="javascript:;" class="a_link choice_list" data-group_id="group_' + group.id + '" data-add_id="' + category.id + '" data-post_title="' + limit_text(_name) + '" data-post_type="categories">選択</a></li>');
            });
        });

    }).fail(function(jqXHR) {
        $('.header_status_text').text('通信エラー');
        $('.header_status').addClass('_show _error');

    }).always(function() {
        setTimeout(function() {
            $('.header_status_text').text('');
            $('.header_status').removeClass('_show _error');
        }, 2000);
    });
}

if ($('#categories_list').length != 0) {
    get_categories();
}

$('.text_list_child').each(function() {
    if ($(this).find('li').length !== 0) {
        $(this).prev().show();
    }
});

$(document).on('click', '.choice_list', function() {
    var add_id = $(this).attr('data-add_id');
    var post_type = $(this).attr('data-post_type');
    var post_title = $(this).attr('data-post_title');
    var group_id = $(this).attr('data-group_id');
    if (group_id) {
        var choice_block = $('#' + group_id);
    } else {
        var choice_block = $(this).parents('td').next().find('ul');
    }

    if ($('#' + post_type + '_' + add_id).length != 0) {
        return false;
    }
    choice_block.prev().show();
    choice_block.append('<li><input type="checkbox" name="' + post_type + '" checked value="' + add_id + '" id="' + post_type + '_' + add_id + '"><label for="' + post_type + '_' + add_id + '">' + post_title + '</label></li>');
});

$('.input_search').keydown(function(e) {
    if ((e.which && e.which === 13) || (e.keyCode && e.keyCode === 13)) {
        $(this).next().click();
        return false;
    } else {
        return true;
    }
});