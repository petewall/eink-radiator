/* eslint-env browser, jquery */

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
  if (data.type === 'select') {
    field.append(buildSelectField(key, data))
  } else if (data.type === 'text') {
    field.append(buildTextField(key, data))
  } else if (data.type === 'textarea') {
    field.append(buildTextArea(key, data))
  }
  return field
}

function buildConfigurationForm(configuration) {
  let fields = [
    $(`<input name="id" value="${configuration.id}" type="hidden" />`),
    buildConfigurationField('name', {type: 'text', value: configuration.name})
  ]
  for (let key in configuration.data) {
    fields.push(buildConfigurationField(key, configuration.data[key]))
  }
  return fields
}

/* exported showImageSourceDetails */
function showImageSourceDetails() {
  const imageSourceId = $(this).attr('id').substring('image_source_'.length)
  $('#image_source_details img.screen').attr('src', `/image_sources/${imageSourceId}/image.png`)

  $.get(`/image_sources/${imageSourceId}/configuration.json`, (configuration) => {
    $('#image_source_details .configuration.form .field').remove()
    $('#image_source_details .configuration.form').prepend(
      buildConfigurationForm(configuration)
    )
    
    $('#image_source_details').modal('show')
  }, 'json')
}

function prepareData(array) {
  let result = {
    data: {}
  }
  for (const field of array) {
    if (field.name == 'id' || field.name == 'name') {
      result[field.name] = field.value
    } else {
      result.data[field.name] = { value: field.value }
    }
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
  $.ajax({
    type: 'POST',
    url: `/image_sources/${data.id}/configuration.json`,
    contentType: 'application/json',
    data: JSON.stringify(data),
    success: (result, status) => {
      if (status == 'nocontent') {
        toggleImageSourceDetailsLoader(false)
      }
    },
    dataType: 'json'
  })
}
