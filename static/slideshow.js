/* eslint-env browser, jquery */
/* exported handleSlideshowEvent */
/*global initial_time_remaining, prepareData */

var time_remaining = initial_time_remaining

function handleSlideshowEvent(data) {
  if (data.slide_activated) {
    $('.slideshow.item').removeClass('selected')
    $(`#image_source_${data.image_source_id}`).addClass('selected')
    time_remaining = data.interval
  }

  if (data.slideshow_changed) {
    updateSlideshowList(data.slides)
  }
}

function updateSlideshowList(slides) {
  // $('#slideshow_list .item').each((_, slide) => {
  //   const imageSourceId = slide.attr('id').substring('image_source_'.length)
  //   if (!$.inArray(imageSourceId, slides)) {
  //     slide.remove()
  //   }
  // })

  for (let i = 0; i < slides.length; i += 1) {
    if ($(`#image_source_${slides[i]}`).length > 0) {
      const slide = $(`#image_source_${slides[i]}`).detach()
      if (i == 0) {
        $('#slideshow_list').prepend(slide)
      } else {
        $(`#image_source_${slides[i - 1]}`).after(slide)
      }
    } else {
      // new slide
    }
  }
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
  $('#slideshow_list').dragndrop({
    onDrop: (slideshow, image_source) => {
      const index = $(slideshow).children().toArray().findIndex((elem) => elem == image_source)
      const imageSourceId = $(image_source).attr('id').substring('image_source_'.length)
      $.ajax({
        type: 'POST',
        url: `/image_sources/${imageSourceId}/set_index?new_index=${index}`
      })
    }
  })
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
  $('#slideshow_details input').keyup(updateSlideshowDurationLabel)

  setInterval(() => {
    if (time_remaining > 0) {
      $('#slideshow_timer').text(secondsToHHMMDD(time_remaining))
      time_remaining -= 1
    }
  }, 1000);
})
