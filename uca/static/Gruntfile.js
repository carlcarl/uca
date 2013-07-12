/*global node:true, module:true*/

module.exports = function (grunt) {
	"use strict";
	// Project configuration.
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		uglify: {
			options: {
				mangle: {
					except: ['jQuery']
				}
			},
			dist: {
				files: {
					'dist/js/index.min.js': ['src/js/jquery-1.8.3.min.js', 'src/js/bootstrap.min.js', 'src/js/index.js']
				}
			}
		},
		cssmin: {
			options: {
				keepSpecialComments: 0
			},
			compress: {
				files: {
					'dist/css/style.css': [
						'src/css/bootstrap.css',
						'src/css/bootstrap-responsive.css',
						'src/css/style.css'
					]
				}
			},
			minify: {
				expand: true,
				cwd: 'dist/css/',
				src: ['*.css', '!*.min.css'],
				dest: 'dist/css/',
				ext: '.min.css'
			}
		},
		watch: {
			css: {
				files: 'src/css/*.css',
				tasks: ['cssmin'],
				options: {
					livereload: true
				}
			},
			js: {
				files: 'src/js/*.js',
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
