function updateWideTables() {

	$('table.widetable').each(function () {

		var wrapper = $('<div class="synaptics-table-wrapper synaptics-table-hidden"><div class="synaptics-table-inner-wrapper"></div></div>');
		$(this).wrapAll(wrapper);

		var tableNum = $($(this).find('caption span')[0]).text()
		var tableCaption = $($(this).find('caption span')[1]).text()
		var caption = $('<p><a href="#">' + tableNum + ': ' + tableCaption + '</a></p>');

		var wrapper = $(this).parent().parent();

		wrapper.before(caption);

		caption.on('click', function () {
			wrapper.removeClass('synaptics-table-hidden')
			return false;
		});

		var close = $('<p><a class="synaptics-close-link" href="#">Close</href></p>');

		close.on('click', function () {
			wrapper.addClass('synaptics-table-hidden')
			return false;
		})

		$(this).before(close)
	});

}

jQuery(updateWideTables);