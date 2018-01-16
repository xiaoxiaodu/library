/**
 * @class W.component.library.Image
 * 
 */

ensureNS('W.component.library');
W.component.library.Image = W.component.Component.extend({
	type: 'library.image',
	selectable: 'no',

	properties: [{
		group: '',
		fields: [{
			name: 'url',
			isUserProperty: true,
			type: 'text',
			displayName: '图片地址',
			default: ''
		}]
	}],

	propertyChangeHandlers: {
		url: function($node, model, value, $propertyViewNode) {
			$node.attr('src', value);
		}
	},

	render: function() {
		var html = '<img class="xui-i-image" data-cid="'+this.cid+'" src="'+ this.model.get('url')+'" />';
		return html;
	}
});
