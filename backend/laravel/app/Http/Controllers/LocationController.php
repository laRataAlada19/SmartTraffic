<?php

namespace App\Http\Controllers;

use App\Models\Location;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\DB;

class LocationController extends Controller
{
    public function index()
    {
        try {
            $locations = Location::all();
            return response()->json($locations, 200);
        } catch (\Exception $e) {
            Log::error('Error fetching locations: ' . $e->getMessage());
            throw $e;
        }
    }

    public function store(Request $request)
    {
        Log::info('Storing a new location', ['request' => $request->all()]);

        $validated = $request->validate([
            'location' => 'required|string|max:255',
            'direction' => 'required|string|max:10',
        ]);

        $location = Location::create([
            'location' => $validated['location'],
            'direction' => $validated['direction'],
        ]);

        return response()->json($location, 201);
    }

    public function show($id)
    {
        $location = Location::find($id);
        if (!$location) {
            return response()->json(['message' => 'Location not found'], 404);
        }
        return response()->json($location);
    }

    public function update(Request $request, $id)
    {
        $location = Location::find($id);
        if (!$location) {
            return response()->json(['message' => 'Location not found'], 404);
        }
        $location->update($request->all());
        return response()->json($location);
    }

    public function destroy($id)
    {
        $location = Location::find($id);
        if (!$location) {
            return response()->json(['message' => 'Location not found'], 404);
        }
        $location->delete();
        return response()->json(['message' => 'Location deleted successfully']);
    }
}
