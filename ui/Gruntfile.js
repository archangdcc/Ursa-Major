module.exports = function(grunt) {
'use strict';

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),

		githash: {
			main: {
				options: {},
			},
		},

		bower: {
			install: {
				options: {
					install: true,
					copy: false
				}
			}
		},

		copy: {
			main: {
				files: [{
					expand: true,
					flatten: true,
					src: [
						'bower_components/**/*.min.js',
						'!bower_components/angular-material/layouts/*.js',
						'!bower_components/angular-messages/*.js',
						'!bower_components/angular-material/modules/**/*.js'
					],
					dest: 'lib/js/'
				}, {
					expand: true,
					flatten: true,
					src: [
						'bower_components/**/*.min.css',
						'!bower_components/angular-material/layouts/*.css',
						'!bower_components/angular-material/modules/**/*.css'
					],
					dest: 'lib/css/'
				}]
			},
			debug: {
				files: [{
					expand: true,
					flatten: true,
					src: ['tmp/um.js'],
					dest: 'lib/js/'
				}, {
					expand: true,
					flatten: true,
					src: ['app/um.css'],
					dest: 'lib/css/'
				}]
			}
		},

		'string-replace': {
			dist: {
				files: {
					'lib/js/um.min.js': 'lib/js/um.min.js',
				},
			},
			options: {
				replacements: [{
					pattern: '__VERSION__',
					replacement: '<%= pkg.version %>',
				}, {
					pattern: '__GIT_HASH__',
					replacement: '<%= githash.main.short %>',
				}]
			},
		},

		uglify: {
			build: {
				files: {
					'lib/js/um.min.js': ['tmp/um.js']
				},
				options:{
					mangle: false
				}
			}
		},

		cssmin: {
			build: {
				files: {
					'lib/css/um.min.css': 'app/um.css'
				}
			}
		},

		usebanner: {
			build: {
				options: {
					position: 'top',
					banner:
						'/*\n' +
						' Ursa Major\n' +
						' (c) 2016  DING Changchang\n' +
						' License: GPLv3\n' +
						'*/',
				},
				files: {
					src: ['lib/js/um.min.js', 'lib/css/um.min.css']
				}
			}
		},

		html2js: {
			options: {
				base: '',
				module: 'templates',
				singleModule: true,
				useStrict: true,
				htmlmin: {
					collapseBooleanAttributes: true,
					collapseWhitespace: true,
					removeAttributeQuotes: true,
					removeComments: true,
					removeEmptyAttributes: true,
					removeRedundantAttributes: true,
					removeScriptTypeAttributes: true,
					removeStyleLinkTypeAttributes: true
				}
			},
			build: {
				src: ['app/**/*.html'],
				dest: 'tmp/templates.js'
			}
		},

		clean: {
			temp: {
				src: ['tmp']
			},
			lib: {
				src: ['lib']
			},
			dist: {
				src: ['dist']
			},
			bower: {
				src: ['bower_components']
			},
			npm: {
				src: ['node_modules']
			},
			um: {
				src: ['lib/js/um.js', 'lib/js/um.min.js', 'lib/css/um.css', 'lib/css/um.min.css']
			}
		},

		concat: {
			options: {
				separator: ';'
			},
			build: {
				src: [
					'app/app.module.js',
					'app/app.config.js',
					'app/app.state.js',
					'app/**/*.js',
					'tmp/*.js'
				],
				dest: 'tmp/um.js'
			}
		},

		jshint: {
			all: ['Gruntfile.js', 'app/*.js', 'app/**/*.js']
		},

		compress: {
			main: {
				options: {
					archive: 'dist/um-ui-<%= pkg.version %>.tar.gz'
				},
				files: [
					{src: ['./index.html', './lib/**', './asset/**'], dest: 'um-ui/'}
				],
			}
		}
	});

	grunt.loadNpmTasks('grunt-contrib-jshint');
	grunt.loadNpmTasks('grunt-contrib-clean');
	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-contrib-cssmin');
	grunt.loadNpmTasks('grunt-contrib-copy');
	grunt.loadNpmTasks('grunt-contrib-compress');
	grunt.loadNpmTasks('grunt-html2js');
	grunt.loadNpmTasks('grunt-bower-task');
	grunt.loadNpmTasks('grunt-banner');
	grunt.loadNpmTasks('grunt-string-replace');
	grunt.loadNpmTasks('grunt-githash');

	grunt.registerTask('prereq', [
		'clean:temp',
		'clean:lib',
		'bower',
		'copy',
		'clean:temp',
	]);
	grunt.registerTask('build', [
		'jshint',
		'clean:um',
		'html2js:build',
		'concat:build',
		'uglify:build',
		'cssmin:build',
		'usebanner:build',
		'clean:temp',
		'clean:dist',
		'githash:main',
		'string-replace:dist',
//		'compress',
	]);
	grunt.registerTask('debug', [
		'jshint',
		'clean:um',
		'html2js:build',
		'concat:build',
		'copy:debug',
		'clean:temp',
		'clean:dist',
	]);
	grunt.registerTask('distclean', [
		'clean:npm',
		'clean:bower',
		'clean:lib',
		'clean:temp',
		'clean:dist',
	]);
};
