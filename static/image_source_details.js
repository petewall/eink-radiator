/* eslint-env browser, jquery */
/*global palette, transforms */

const colorIcons = {
  WHITE: 'circle outline',
  BLACK: 'circle',
  RED: 'red cirle'
}

function buildColorField(key, data) {
  const field = $('<div class="grouped fields">')
  for (const color of palette) {
    const radio = $(`<input type="radio" name="${key}" value="${color}">`)
    const label = $(`<label><i class="${colorIcons[color]} circle icon"></i>${color}</label>`)

    if (color == data.value) {
      radio.attr('checked', true)
    }

    field.append(
      $('<div class="field">').append(
        $('<div class="ui radio checkbox">').append(radio, label)
      )
    )
  }
  return field
}

function buildHiddenField(key, data) {
  return $(`<input name="${key}" class="field" value="${data.value}" type="hidden" />`)
}

function buildSelectField(key, data) {
  const dropdown = $(`<select name="${key}" class="ui selection dropdown">`)
  for (const option of data.options) {
    dropdown.append($(`<option value="${option}">${option}</option>`).attr('selected', option == data.value))
  }

  dropdown.dropdown()
  return dropdown
}

function buildTextArea(key, data) {
  const field = $(`<textarea name="${key}">`)
  field.val(data.value)
  return field
}

function buildTextField(key, data) {
  return $(`<input name="${key}" value="${data.value}" type="text" />`)
}

const transformIcons = {
  NONE: 'expand',
  FLIP_LEFT_RIGHT: 'arrows alternate horizontal',
  FLIP_TOP_BOTTOM: 'arrows alternate vertical',
  ROTATE_180: 'sync alternate',
}

function buildTransformField(key, data) {
  const field = $('<div class="grouped fields">')
  for (const transform of transforms) {
    const radio = $(`<input type="radio" name="${key}" value="${transform}">`)
    const label = $(`<label><i class="${transformIcons[transform]} icon"></i>${transform}</label>`)

    if (transform == data.value) {
      radio.attr('checked', true)
    }

    field.append(
      $('<div class="field">').append(
        $('<div class="ui radio checkbox">').append(radio, label)
      )
    )
  }
  return field
}

function buildConfigurationField(key, data) {
  const field = $('<div class="field">')
  field.append($('<label>').text(key))
  if (data.type === 'hidden') {
    field.empty()
    field.append(buildHiddenField(key, data))
  } else if (data.type === 'color') {
    field.append(buildColorField(key, data))
  } else if (data.type === 'select') {
    field.append(buildSelectField(key, data))
  } else if (data.type === 'text') {
    field.append(buildTextField(key, data))
  } else if (data.type === 'textarea') {
    field.append(buildTextArea(key, data))
  } else if (data.type === 'transform') {
    field.append(buildTransformField(key, data))
  }
  return field
}

function buildConfigurationForm(configuration) {
  const fields = []
  for (const key in configuration.data) {
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
      buildHiddenField('id', {value: imageSourceId}),
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

  const data = prepareData($('#image_source_details form').serializeArray())
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

function showImageSource() {
  const data = prepareData($('#image_source_details form').serializeArray())
  $.post(`/image_sources/${data.data.id.value}/activate`)
}

/* exported handleImageSourceEvent */
function handleImageSourceEvent(data) {
  const id = data.image_source_id
  $(`#image_source_${id} img`).attr('src', `/image_sources/${id}/image.png?timestamp=${new Date().getTime()}`)

  // TODO: Only update the details if the updated image_source is the one open
  $('#image_source_details img.screen').attr('src', `/image_sources/${id}/image.png?timestamp=${new Date().getTime()}`)
  $('#image_source_details img.screen').off('load')
  $('#image_source_details img.screen').on('load', () => {
    toggleImageSourceDetailsLoader(false)
  })
}

$(document).ready(() => {
  $('.slideshow.image_source.item').click(showImageSourceDetails)
  $('#image_source_details .save.button').click(saveImageSourceDetails)
  $('#image_source_details .show.button').click(showImageSource)
})
