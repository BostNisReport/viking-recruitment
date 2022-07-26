"user strict";

$(window).load(function(){
    // Get middlewaretoken to post it.
    var middleware_token = $('input[name="csrfmiddlewaretoken"]').val();

    var filters_ids = [
        'id_rank', 'id_nationality', 'id_vessel_type_experience', 'id_current_location',
        'id_languages', 'id_coc_certificate', 'id_coc_issuing_authority', 'id_marine_certificate',
        'id_additional_certification'
    ];
    
    function update_select_filters(){
        $(filters_ids).each(function(index, key){
            // Filters name
            name = key.replace('id_', '').replace(/_/g, ' ');
            SelectFilter.init(key, name, false, '/static/admin/');
    
        });
    }
    
    update_select_filters();

    $select_box = $('.select-preference');
      // Append new preference in select box.
    function update_select_box(name, id){
      $select_box.append('<option value="'+id+'">'+ name +'</option>');
    }

    // Display model when save search clicked.
    $(document).on('click', '.save-search', function(e){
      e.preventDefault();
      $('#save-search-modal').modal('show');
    });


    // Remove attribute disabled if form has been changed.
    $('#candidate_search').change(function(){
        $('.save-search').removeAttr('disabled');
    });


    // Save preference.
    $('.save-preference').click(function(){

        // Select values.
        $(filters_ids).each(function(index, key){
            // Filters name
            // SelectBox.select_all(key + '_to');
        });

        data = [];

        $search_preferences_form = $('.search-preferences-form');

        //  Serialzie search query.
        var search_query = $('#candidate_search').serialize();

        // New preference name.
        var search_query_name = $search_preferences_form.find('#id_name').val();

        $.post(SAVE_SEARCH_URL, {
          'csrfmiddlewaretoken': middleware_token,
          'name': search_query_name,
          'search_query': search_query,
        }, function(json) {

          if ('success' in json){
            // Hide modal.
            $('#save-search-modal').modal('hide');

            // Update select box with new preference
            if (json.created){
                update_select_box(search_query_name, json.id);
            }

          } else {
            // Display error message.
            $help_block = $search_preferences_form.find('.help-block');
            $help_block.text(json.data.name.join(''));
          }
        });
    });

    // Choosing one of prereferece fires event to get pereferences.
    $('.select-preference').on('change', function(e){
        var option_selected = $("option:selected", this);
        var value_selected = option_selected.attr('value');
        if (value_selected > 0){
            var active_tab = $('.form-wrapper').find('fieldset.active').index();

            $.get(GET_PREFERENCE_URL, {
                'id': value_selected, 'active_tab':active_tab
            }, function(json) {
                var active_tab = parseInt(json.active_tab);
                $('.form-wrapper').html(json.form);
                $('.form-wrapper fieldset').eq(active_tab).addClass('active');
                update_select_filters();
            });
        } else {
            return false;
        }
    });

    // Remove attribute disabled from button when preference is selected.
    $('.select-preference').change(function(){
      $('.delete-preference').removeAttr('disabled');
    });

    // Delete preference.
    $('.delete-preference').click(function(e){
      e.preventDefault();

      var option_selected = $('.select-preference option:selected');
      var preference_id = option_selected.val();

      $.post(DELETE_PREFERENCE_URL, {
        'id': preference_id,
        'csrfmiddlewaretoken': middleware_token,
      }, function(json) {
        option_selected.remove();
        // Select default value.
        $('.select-preference .default-preference').prop('selected', true);

        // Disable delete preference button if there is no options.
        if ( $(this).children('option').length <= 1) {
          $('.delete-preference').attr('disabled','disabled');
        }
      });

    });


});
