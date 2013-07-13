/*global node:true, module:true*/

module.exports = function (grunt) {
	"use strict";
	// Project configuration.
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		uglify: {
			release: {
				files: {
					'uca/static/dist/js/index.min.js': ['uca/static/src/js/jquery-1.8.3.min.js', 'uca/static/src/js/bootstrap.min.js', 'uca/static/src/js/index.js']
				}
			}
		},
		cssmin: {
			options: {
				keepSpecialComments: 0
			},
			release: {
				files: {
					'uca/static/dist/css/style.min.css': [
						'uca/static/src/css/bootstrap.css',
						'uca/static/src/css/bootstrap-responsive.css',
						'uca/static/src/css/style.css'
					]
				}
			}
		},
		watch: {
			css: {
				files: 'uca/static/src/css/*.css',
				tasks: ['cssmin'],
				options: {
					livereload: true
				}
			},
			js: {
				files: 'uca/static/src/js/*.js',
				tasks: ['uglify'],
				options: {
					livereload: true
				}
			}
		}
	});

	// Load the plugins
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-contrib-cssmin');
	grunt.loadNpmTasks('grunt-contrib-watch');

	// Default task(s).
	grunt.registerTask('default', ['uglify', 'cssmin', 'watch']);

};
