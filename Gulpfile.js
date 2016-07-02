var gulp = require('gulp');
var concat = require('gulp-concat');

gulp.task('concat', function() {
    return gulp.src(['./blocks/commands.py', './blocks/engine.py'])
        .pipe(concat('main.py'))
        .pipe(gulp.dest('./'));
});

gulp.task('watch', function() {
    gulp.watch('./blocks/*.py', ['concat']);
});

gulp.task('default', ['concat','watch']);
