/* eslint-env browser, jquery */

function buildHiddenField(key, data) {
  return $(`<input name="${key}" class="field" value="${data.value}" type="hidden" />`)
}

function buildSelectField(key, data) {
  let dropdown = $(`<select name="${key}" class="ui selection dropdown">`)
  for (let option of data.options) {
    dropdown.append($(`<option value="${option}">${option}</option>`).attr('selected', option == data.value))
  }

  dropdown.dropdown()
  return dropdown
}

function buildTextArea(key, data) {
  let field = $(`<textarea name="${key}">`)
  field.val(data.value)
  return field
}

function buildTextField(key, data) {
  return $(`<input name="${key}" value="${data.value}" type="text" />`)
}

function buildConfigurationField(key, data) {
  let field = $('<div class="field">')
  field.append($('<label>').text(key))
  if (data.type === 'hidden') {
    field.empty()
    field.append(buildHiddenField(key, data))
  } else if (data.type === 'select') {
    field.append(buildSelectField(key, data))
  } else if (data.type === 'text') {
    field.append(buildTextField(key, data))
  } else if (data.type === 'textarea') {
    field.append(buildTextArea(key, data))
  }
  return field
}

function buildConfigurationForm(configuration) {
  let fields = []
  for (let key in configuration.data) {
    fields.push(buildConfigurationField(key, configuration.data[key]))
  }
  return fields
}

/* exported showImageSourceDetails */
function showImageSourceDetails() {
  const imageSourceId = $(this).attr('id').substring('image_source_'.length)
  $('#image_source_details img.screen').attr('src', `/image_sources/${imageSourceId}/image.png?timestamp=${new Date().getTime()}`)

  $.get(`/image_sources/${imageSourceId}/configuration.json`, (configuration) => {
    $('#image_source_details .configuration.form').empty()
    $('#image_source_details .configuration.form').append(
      buildConfigurationForm(configuration)
    )
    
    toggleImageSourceDetailsLoader(false)
    $('#image_source_details').modal('show')
  }, 'json')
}

function prepareData(array) {
  const result = {
    data: {}
  }
  for (const field of array) {
    result.data[field.name] = { value: field.value }
  }
  return result
}

function toggleImageSourceDetailsLoader(state) {
  $('#image_source_details .dimmer').toggleClass('disabled', !state)
  $('#image_source_details .dimmer').toggleClass('active', state)
  $('#image_source_details .save.button').attr('disabled', state)
}

function saveImageSourceDetails() {
  toggleImageSourceDetailsLoader(true)

  let data = prepareData($('#image_source_details form').serializeArray())
  const image_source_id = data.data.id.value
  $.ajax({
    type: 'POST',
    url: `/image_sources/${image_source_id}/configuration.json`,
    contentType: 'application/json',
    data: JSON.stringify(data),
    error: (xhr, status, error) => {
      console.error(`failed to save configuration: ${status}: ${error}`)
    },
    success: (result, status) => {
      if (status == 'nocontent') {
        toggleImageSourceDetailsLoader(false)
      } else if (status == 'success') {
        $(`#image_source_${image_source_id} .content`).text(result.data.name.value)
      }
    },
    dataType: 'json'
  })
}

function handleImageSourceEvent(data) {
  const id = data.image_source_id
  $(`#image_source_${id} img`).attr('src', `/image_sources/${id}/image.png?timestamp=${new Date().getTime()}`)

  // TODO: Only update the details if the updated image_source is the one open
  $('#image_source_details img.screen').attr('src', `/image_sources/${id}/image.png?timestamp=${new Date().getTime()}`)
  toggleImageSourceDetailsLoader(false)
}

$(document).ready(() => {
  $('.slideshow.image_source.item').click(showImageSourceDetails)
  $('#image_source_details .save.button').click(saveImageSourceDetails)
})
