module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    sass: {
      options: {
        includePaths: [
          'odalc/static/bower_components/foundation/scss',
        ]
      },
      dist: {
        options: {
          outputStyle: 'compressed'
        },
        files: {
          'odalc/static/base/css/app.css': 'odalc/static/base/scss/app.scss',
          'odalc/static/base/css/courses.css': 'odalc/static/base/scss/courses.scss',
          'odalc/static/base/css/forms.css': 'odalc/static/base/scss/forms.scss'
        }
      }
    },

    watch: {
      grunt: { files: ['Gruntfile.js'] },

      sass: {
        files: 'odalc/static/**/*.scss',
        tasks: ['sass']
      }
    }
  });

  grunt.loadNpmTasks('grunt-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('build', ['sass']);
  grunt.registerTask('default', ['build','watch']);
}
