(function() {
	'use strict';

	angular
		.module('um', [])
		.controller('MainController', MainController);

	MainController.$inject = ['UMService'];

	function MainController(share) {
		var vm = this;

		vm.freeze = false;
		vm.table = share.table;
		vm.history = share.history;
		vm.style = share.style;
		vm.result = share.result;

		vm.make_move = make_move;
		vm.undo = undo;
		vm.umfirst = umfirst;

		function make_move(move) {
			if (vm.freeze)
				return;
			vm.freeze = true;

			share.make_move(move);
			share.get_move().then(
				function () {
					if (vm.result.code == -1)
						vm.freeze = false;
				}
			);
		}

		function undo() {
			var move = vm.history.pop();
			vm.table[move].pop();
			move = vm.history.pop();
			vm.table[move].pop();
		}

		function umfirst() {
			vm.freeze = true;
			share.get_move().then(
				function () {
					vm.freeze = false;
				}
			);
		}
	}
})();
