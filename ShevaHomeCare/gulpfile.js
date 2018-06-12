var gulp = require('gulp');
gulp.task('copy', function () {
    gulp.src('./node_modules/syncfusion-javascript/**')
        .pipe(gulp.dest('./wwwroot/lib/syncfusion-javascript'));
});