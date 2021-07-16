function buildSelectField(key, value) {
  let options = []
  for (let option of value.options) {
    options.push({
      name: option,
      value: option,
      selected: option == value.value
    })
  }

  let dropdown = $('<div class="ui selection dropdown">')
  dropdown.append(
    $('<i class="dropdown icon"></i>'),
    $('<div class="text"></div>')
  )
  dropdown.dropdown({
    values: options
  })
  return dropdown
}

function buildTextArea(key, value) {
  field = $(`<textarea name="${key}">`)
  field.val(value.value)
  return field
}

function buildTextField(key, value) {
  return $(`<input name="${key}" value="${value}" type="text" />`)
}

function buildConfigurationField(key, value) {
  let field = $('<div class="field">')
  field.append($('<label>').text(key))
  if (typeof value === 'string') {
    field.append(buildTextField(key, value))
  } else if (value.type === 'select') {
    field.append(buildSelectField(key, value))
  } else if (value.type === 'textarea') {
    field.append(buildTextArea(key, value))
  }
  return field
}

function buildConfigurationForm(configuration) {
  let fields = []
  for (let key in configuration) {
    fields.push(buildConfigurationField(key, configuration[key]))
  }
  return fields
}

function showImageSourceDetails() {
  const imageSourceId = $(this).attr('id').substring('image_source_'.length)
  $('#image_source_details img.screen').attr('src', `/image_sources/${imageSourceId}/image.png`)

  $.get(`/image_sources/${imageSourceId}/configuration.json`, (configuration) => {
    $('#image_source_details .configuration.form').empty()
    $('#image_source_details .configuration.form').append(
      buildConfigurationForm(configuration)
    )
    $('#image_source_details').modal('show')
  }, 'json')
}
