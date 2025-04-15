<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\LocationController;
use Illuminate\Support\Facades\DB;

Route::get('/locations', [LocationController::class, 'index']);
Route::post('/location', [LocationController::class, 'store']);
Route::get('/locations/{id}', [LocationController::class, 'show']);
Route::patch('/locations/{id}', [LocationController::class, 'update']);
Route::delete('/locations/{id}', [LocationController::class, 'destroy']);
