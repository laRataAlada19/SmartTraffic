<?php

namespace App\Http\Controllers;

use App\Models\Location;
use Illuminate\Support\Facades\Log;
use App\Http\Requests\CreateLocationRequest;
use App\Http\Requests\IndexLocationRequest;
use App\Http\Requests\UpdateLocationRequest;

class LocationController extends Controller
{
    public function index(IndexLocationRequest $request)
    {
        try {
            $query = Location::query();

            if ($request->filled('location')) {
                $query->where('location', 'like', '%' . $request->location . '%');
            }

            if ($request->filled('direction')) {
                $query->where('direction', 'like', '%' . $request->direction . '%');
            }

            if ($request->filled('sort_by') && $request->filled('sort_order')) {
                $query->orderBy($request->sort_by, $request->sort_order);
            }

            $locations = $query->paginate($request->input('per_page', 20));
            
            return response()->json([
                'data' => $locations->items(),
                'meta' => [
                    'current_page' => $locations->currentPage(),
                    'last_page' => $locations->lastPage(),
                    'per_page' => $locations->perPage(),
                    'total' => $locations->total(),
                ],
            ]);
        } catch (\Exception $e) {
            Log::error('Error fetching locatsadasions: ' . $e->getMessage());
            return response()->json(['message' => 'Error fetching locations'], 500);
        }
    }

    public function store(CreateLocationRequest $request)
    {
        try {
            $location = Location::create($request->validated());
            return response()->json($location, 201);
        } catch (\Exception $e) {
            Log::error('Error creating location: ' . $e->getMessage());
            return response()->json(['message' => 'Error creating location' . $e->getMessage()], 500);
        }
    }

    public function show($id)
    {
        try {
            $location = Location::find($id);
            return response()->json($location);
        } catch (\Exception $e) {
            Log::error('Error fetching location: ' . $e->getMessage());
            return response()->json(['message' => 'Error fetching location'], 500);
        }
    }

    public function update(UpdateLocationRequest $request, $id)
    {
        try {
            $location = Location::find($id);
            $location->update($request->validate());
            return response()->json($location, 200);
        } catch (\Exception $e) {
            Log::error('Error updating location: ' . $e->getMessage());
            return response()->json(['message' => 'Error updating location'], 500);
        }
    }

    public function destroy($id)
    {
        try {
            $location = Location::find($id);
            $location->delete();
            return response()->json(['message' => 'Location deleted successfully'], 204);
        } catch (\Exception $e) {
            Log::error('Error deleting location: ' . $e->getMessage());
            return response()->json(['message' => 'Error deleting location'], 500);
        }
    }
}