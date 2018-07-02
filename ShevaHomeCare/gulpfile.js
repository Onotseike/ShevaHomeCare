var gulp = require('gulp');
//var ts = require('gulp-typescript');
//var sourcemaps = require('gulp-sourcemaps');
//var tslint = require("gulp-tslint");
//var minify = require('gulp-minify');
//var git = require('gulp-git');
//var versionBump = require('gulp-bump')
//var tagVersion = require('gulp-tag-version');
//var webpack = require('webpack-stream');

gulp.task('copy', function () {
    gulp.src('./node_modules/syncfusion-javascript/**')
        .pipe(gulp.dest('./wwwroot/lib/syncfusion-javascript'));
    gulp.src('./node_modules/jsrender/**')
        .pipe(gulp.dest('./wwwroot/lib/jsrender'));
    gulp.src('./node_modules/microsoft-speech-browser-sdk/**')
        .pipe(gulp.dest('./wwwroot/lib/microsoft-speech-browser-sdk'));
    gulp.src('./node_modules/webpack/**')
        .pipe(gulp.dest('./wwwroot/lib/webpack'));
});

//gulp.task("build_ES5", function () {
//    return gulp.src([
//        "./lib/microsoft-speech-browser-sdk/src/**/*.ts",
//        "Speech.Browser.Sdk.ts"],
//        { base: '.' })
//        .pipe(tslint({
//            formatter: "prose",
//            configuration: "tslint.json"
//        }))
//        .pipe(tslint.report({
//            summarizeFailureOutput: true
//        }))
//        .pipe(sourcemaps.init())
//        .pipe(ts({
//            target: "ES5",
//            declaration: true,
//            noImplicitAny: true,
//            removeComments: false,
//            outDir: 'distrib'
//        }))
//        .pipe(sourcemaps.write('.'))
//        .pipe(gulp.dest('distrib'));
//});


//gulp.task("build", ["build_ES5"]);

//gulp.task("bundle", ["build_ES5"], function () {
//    return gulp.src('samples/browser/sample_app.js')
//        .pipe(webpack({
//            output: { filename: 'speech.sdk.bundle.js' },
//            devtool: 'source-map',
//            module: {
//                rules: [{
//                    enforce: 'pre',
//                    test: /\.js$/,
//                    loader: "source-map-loader"
//                }]
//            }
//        }))
//        .pipe(gulp.dest('distrib'));
//});


//// We don't want to release anything without a successful build. So build task is dependency for these tasks.
//gulp.task('patchRelease', ['build'], function () { return BumpVersionTagAndCommit('patch'); })
//gulp.task('featureRelease', ['build'], function () { return BumpVersionTagAndCommit('minor'); })
//gulp.task('majorRelease', ['build'], function () { return BumpVersionTagAndCommit('major'); })
//gulp.task('preRelease', ['build'], function () { return BumpVersionTagAndCommit('prerelease'); })

//function BumpVersionTagAndCommit(versionType) {
//    return gulp.src(['./package.json'])
//        // bump the version number
//        .pipe(versionBump({ type: versionType }))
//        // save it back to filesystem 
//        .pipe(gulp.dest('./'))
//        // commit the changed version number 
//        .pipe(git.commit('Bumping package version'))
//        // tag it in the repository
//        .pipe(tagVersion());
//}