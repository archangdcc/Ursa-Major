(function() {
	'use strict';

	angular
		.module('um')
		.service('UMService', UMService);

	UMService.$inject = ['$http'];

	function UMService($http) {
		/* jshint validthis: true */
		var self = this;

		self.history = [];
		self.table = [[], [], [], [], [], [], []];
		self.style = [[], [], [], [], [], [], []];
		self.result = {code: -1, message: ''};
		self.player = 0;

		self.make_move = make_move;
		self.get_move = get_move;

		function make_move(move) {
			if (self.table[move].length == 6)
				return;
			self.history.push(move);
			self.table[move].push(self.player);
			self.player = 1 - self.player;
		}

		function get_move() {
			return $http.post('/um-api', {moves: self.history}).then(
				function (response) {
					var i, c, r;
					self.result.code = response.data.result;
					switch (response.data.result) {
					case 2:
						for(i = 0; i < 4; i++) {
							c = response.data.positions[i][0];
							r = response.data.positions[i][1];
							self.style[c][r] = {color: 'red'};
						}
						self.make_move(response.data.move);
						self.result.message = "Ursa Major Win!";
						break;
					case 0:
						for(i = 0; i < 4; i++) {
							c = response.data.positions[i][0];
							r = response.data.positions[i][1];
							self.style[c][r] = {color: 'red'};
						}
						self.result.message = "You Win!";
						break;
					case 1:
						self.result.message = "Draw!";
						if (response.data.move !== undefined)
							self.make_move(response.data.move);
						break;
					default:
						self.make_move(response.data.move);
						break;
					}
				}, function (errResponse) {
					console.error("Error getting move.");
				}
			);
		}
	}
})();
