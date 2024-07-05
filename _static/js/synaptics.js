function updateWideTables() {

	$('table.widetable').each(function () {

		var wrapper = $('<div class="synaptics-table-wrapper synaptics-table-hidden"><div class="synaptics-table-inner-wrapper"></div></div>');
		$(this).wrapAll(wrapper);

		var tableCaption = $($(this).find('caption span')[0]).text()
		var caption = $('<div class="synaptics-table-placeholder"><div class="synaptics-table-caption">' + tableCaption + '</div><a href="#"><div class="synaptics-table-icon">▦</div></a></div>');

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
