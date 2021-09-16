/* eslint-env browser, jquery */

function handleSlideshowEvent(data) {
  $('.slideshow.item').removeClass('selected')
  $(`.slideshow.item:eq(${data.image_source_index})`).addClass('selected')
  time_remaining = data.interval
}

function secondsToHHMMDD(seconds) {
  return new Date(seconds * 1000).toISOString().substr(11, 8)
}

function updateSlideshowDurationLabel() {
  const duration = $('#slideshow_details input').val()
  $('#slideshow_details input + div.label').text(secondsToHHMMDD(duration))
}

function saveSlideshowDetails() {
  const data = prepareData($('#slideshow_details form').serializeArray())
  $.ajax({
    type: 'POST',
    url: `/slideshow/configuration.json`,
    contentType: 'application/json',
    data: JSON.stringify(data),
    error: (xhr, status, error) => {
      console.error(`failed to save configuration: ${status}: ${error}`)
    },
    success: () => {
      $('#slideshow_details').modal('hide')
    },
    dataType: 'json'
  })

}

$(document).ready(() => {
  $('.controls .previous.button').click(() => {
    $.post('/slideshow/previous')
  })
  $('.controls .next.button').click(() => {
    $.post('/slideshow/next')
  })
  $('.controls #slideshow_timer').click(() => {
    $.get('/slideshow/configuration.json', (configuration) => {
      const interval = parseInt(configuration.data['interval'].value, 10)
      $('#slideshow_details input').val(interval)
      updateSlideshowDurationLabel()
      $('#slideshow_details').modal('show')
    }, 'json')
  })
  $('#slideshow_details .save.button').click(saveSlideshowDetails)

  updateSlideshowDurationLabel()
  $('#slideshow_details input').change(updateSlideshowDurationLabel)

  setInterval(() => {
    if (time_remaining > 0) {
      $('#slideshow_timer').text(secondsToHHMMDD(time_remaining))
      time_remaining -= 1
    }
  }, 1000);
})
