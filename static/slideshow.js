/* eslint-env browser, jquery */

function handleSlideshowEvent(data) {
  $('.slideshow.item').removeClass('selected')
  $(`.slideshow.item:eq(${data.image_source_index})`).addClass('selected')
  time_remaining = data.interval
}

function secondsToHHMMDD(seconds) {
  return new Date(seconds * 1000).toISOString().substr(11, 8)
}

$(document).ready(() => {
  $(".controls .previous.button").click(() => {
    $.post('/slideshow/previous')
  })
  $(".controls .next.button").click(() => {
    $.post('/slideshow/next')
  })

  setInterval(() => {
    if (time_remaining > 0) {
      $('#slideshow_timer').text(secondsToHHMMDD(time_remaining))
      time_remaining -= 1
    }
  }, 1000);
})
