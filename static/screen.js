/* eslint-env browser, jquery */

/* exported handleScreenEvent */
function handleScreenEvent(data) {
  $(".controls .previous.button").toggleClass("disabled", data.screen_busy)
  $(".controls .next.button").toggleClass("disabled", data.screen_busy)

  $("#image_source_details .actions .show.button").toggleClass("disabled", data.screen_busy)

  $("#screen_content .dimmer").toggleClass("active", data.screen_busy)
  $("#screen_content .dimmer").toggleClass("disabled", !data.screen_busy)
  if (!data.screen_busy) {
    $("#screen_content img").attr("src", `/screen/image.png?timestamp=${new Date().getTime()}`)
  }
}
