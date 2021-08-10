/* eslint-env browser, jquery */

function handleSlideshowEvent(data) {
  $('.slideshow.item').removeClass('selected')
  $(`.slideshow.item:eq(${data.image_source_index})`).addClass('selected')
}

$(document).ready(() => {
  $(".controls .previous.button").click(() => {
    $.post('/slideshow/previous')
  })
  $(".controls .next.button").click(() => {
    $.post('/slideshow/next')
  })
})
