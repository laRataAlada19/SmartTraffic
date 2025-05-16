<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\LocationController;
use App\Http\Controllers\SupersetController;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\UserController; 
use Illuminate\Support\Facades\DB;

Route::get('/locations', [LocationController::class, 'index']);
Route::post('/locations', [LocationController::class, 'store']);
Route::get('/locations/{id}', [LocationController::class, 'show']);
Route::patch('/locations/{id}', [LocationController::class, 'update']);
Route::delete('/locations/{id}', [LocationController::class, 'destroy']);


Route::post('/auth/login', [AuthController::class, 'login']);

Route::get('/superset-token', [SupersetController::class, 'getSupersetToken']);

Route::middleware(['auth:sanctum'])->group(function () {

    Route::post('/auth/logout', [AuthController::class, 'logout']);
    Route::post('/auth/refreshtoken', [AuthController::class, 'refreshToken']);
    Route::get('/users/me', [UserController::class, 'showMe']); // Ensure the UserController class has a 'showMe' method
});