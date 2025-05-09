<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\LocationController;
use App\Http\Controllers\SupersetController;
use App\Http\Controllers\AuthController;
use Illuminate\Support\Facades\DB;

Route::get('/locations', [LocationController::class, 'index']);
Route::post('/locations', [LocationController::class, 'store']);
Route::get('/locations/{id}', [LocationController::class, 'show']);
Route::patch('/locations/{id}', [LocationController::class, 'update']);
Route::delete('/locations/{id}', [LocationController::class, 'destroy']);


Route::post('/auth/login', [AuthController::class, 'login']);

Route::get('/superset-token', [SupersetController::class, 'getSupersetToken']);
